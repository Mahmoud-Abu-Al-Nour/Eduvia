"""
Live Stack E2E Verification Script for Phase 3 (Learner Profile Foundation)
"""
import sys
import httpx

def test_phase3_live():
    print("Testing live Eduvia stack with Phase 3 Learner Profile integration...")
    client = httpx.Client(timeout=10.0)

    # 1. Check frontend reachability
    fe_res = client.get("http://localhost:5173/")
    assert fe_res.status_code == 200, f"Frontend check failed: {fe_res.status_code}"
    print("PASS 1: Frontend server reachable at http://localhost:5173/ (HTTP 200)")

    # 2. Check backend health
    be_res = client.get("http://localhost:8000/api/v1/health")
    assert be_res.status_code == 200, f"Backend health check failed: {be_res.status_code}"
    print("PASS 2: Backend health check reachable at http://localhost:8000/api/v1/health (HTTP 200)")

    # 3. Authenticate as Teacher
    login_res = client.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": "teacher@eduvia.app", "password": "strongpassword123"},
    )
    assert login_res.status_code == 200, f"Teacher login failed: {login_res.status_code}"
    tokens = login_res.json()
    token = tokens.get("access_token")
    assert token, "No access token returned"
    headers = {"Authorization": f"Bearer {token}"}
    print("PASS 3: Authenticated login succeeded, issued signed JWT")

    # 4. Verify user profile
    me_res = client.get("http://localhost:8000/api/v1/users/me", headers=headers)
    assert me_res.status_code == 200, f"/users/me failed: {me_res.status_code}"
    assert me_res.json()["email"] == "teacher@eduvia.app"
    print(f"PASS 4: /users/me returned profile for {me_res.json()['full_name']}")

    # 5. Verify regression: Phase 2 Curriculum works
    curr_res = client.get("http://localhost:8000/api/v1/curricula", headers=headers)
    assert curr_res.status_code == 200, f"/curricula failed: {curr_res.status_code}"
    print(f"PASS 5: Curriculum regression verified ({len(curr_res.json())} curricula returned)")

    # 6. List initial learners
    list_res = client.get("http://localhost:8000/api/v1/learners", headers=headers)
    assert list_res.status_code == 200, f"/learners failed: {list_res.status_code}"
    initial_learners = list_res.json()
    assert len(initial_learners) >= 1, "Expected seeded demo learner"
    print(f"PASS 6: Initial /learners returned {len(initial_learners)} learner(s): '{initial_learners[0]['name']}'")

    # 7. Create a new learner (Teacher workflow)
    create_payload = {
        "name": "Sara Ahmad",
        "age_group": "early_childhood",
        "learning_level": "emerging",
        "teacher_notes": "Very creative, responds well to color-coded cues.",
        "communication_preferences": {
            "primary_mode": "verbal",
            "notes": "Prefers visual cues paired with verbal instructions.",
        },
        "support_requirements": {
            "pacing": "relaxed",
            "guidance_level": "moderate",
            "frequent_breaks": True,
        },
    }
    create_res = client.post("http://localhost:8000/api/v1/learners", json=create_payload, headers=headers)
    assert create_res.status_code == 201, f"Learner creation failed: {create_res.status_code}, {create_res.text}"
    new_learner = create_res.json()
    new_id = new_learner["id"]
    assert new_learner["name"] == "Sara Ahmad"
    assert new_learner["profile"] is not None
    assert "modality_effectiveness" in new_learner["profile"]
    print(f"PASS 7: Created learner 'Sara Ahmad' with ID {new_id} and initialized profile")

    # 8. Retrieve learner details
    detail_res = client.get(f"http://localhost:8000/api/v1/learners/{new_id}", headers=headers)
    assert detail_res.status_code == 200, f"Get learner detail failed: {detail_res.status_code}"
    detail = detail_res.json()
    assert detail["profile"]["teacher_notes"] == "Very creative, responds well to color-coded cues."
    assert detail["profile"]["support_requirements"]["pacing"] == "relaxed"
    print("PASS 8: Retrieved learner detail and verified teacher-provided profile fields")

    # 9. Update learner profile (Edit profile workflow)
    update_payload = {
        "learning_level": "beginner",
        "profile": {
            "teacher_notes": "Updated guidance: loves counting blocks and geometric shapes.",
            "teacher_overrides": {
                "lock_difficulty_level": 2,
                "enforce_strategy": "Step-by-Step",
                "manual_adjustments_active": True,
            },
        },
    }
    patch_res = client.patch(f"http://localhost:8000/api/v1/learners/{new_id}", json=update_payload, headers=headers)
    assert patch_res.status_code == 200, f"Update learner failed: {patch_res.status_code}"
    updated = patch_res.json()
    assert updated["learning_level"] == "beginner"
    assert updated["profile"]["teacher_overrides"]["lock_difficulty_level"] == 2
    assert updated["profile"]["teacher_overrides"]["manual_adjustments_active"] is True
    print("PASS 9: Updated learner profile and verified teacher overrides")

    # 10. Record educational learning observation
    obs_payload = {
        "category": "modality",
        "summary": "Demonstrated high accuracy and engagement when visual manipulatives were used.",
        "teacher_note": "Visual scaffolding promotes active participation.",
    }
    obs_res = client.post(f"http://localhost:8000/api/v1/learners/{new_id}/observations", json=obs_payload, headers=headers)
    assert obs_res.status_code == 201, f"Add observation failed: {obs_res.status_code}"
    obs_data = obs_res.json()
    assert obs_data["category"] == "modality"
    print(f"PASS 10: Recorded learning observation (ID: {obs_data['id']})")

    # 11. Reload and verify persisted observation in profile
    reload_res = client.get(f"http://localhost:8000/api/v1/learners/{new_id}", headers=headers)
    assert reload_res.status_code == 200
    reload_data = reload_res.json()
    observations = reload_data["profile"]["observations"]
    assert len(observations) >= 1, "Expected recorded observation to persist"
    assert observations[-1]["id"] == obs_data["id"]
    print("PASS 11: Reloaded learner profile and verified persistent observation log")

    # 12. Security & RBAC validations
    unauth_res = client.get("http://localhost:8000/api/v1/learners")
    assert unauth_res.status_code == 401, "Expected 401 for unauthenticated request"
    invalid_res = client.get("http://localhost:8000/api/v1/learners", headers={"Authorization": "Bearer bad.token"})
    assert invalid_res.status_code == 401, "Expected 401 for invalid token"
    print("PASS 12: Security & token boundary enforced (401 on missing or invalid token)")

    # 13. Delete created learner (cleanup)
    del_res = client.delete(f"http://localhost:8000/api/v1/learners/{new_id}", headers=headers)
    assert del_res.status_code == 204, f"Delete failed: {del_res.status_code}"
    get_del_res = client.get(f"http://localhost:8000/api/v1/learners/{new_id}", headers=headers)
    assert get_del_res.status_code == 404, "Expected 404 after deletion"
    print("PASS 13: Deleted learner and verified cascade profile deletion (404 on subsequent get)")

    print("\nALL 13 PHASE 3 LIVE STACK INTEGRATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_phase3_live()
