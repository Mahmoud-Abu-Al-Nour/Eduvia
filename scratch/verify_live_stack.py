import httpx
import sys

def test_live_stack():
    print("Testing live Eduvia services...")
    
    # 1. Frontend Server
    with httpx.Client(timeout=10.0) as client:
        fe_res = client.get("http://localhost:5173/")
        assert fe_res.status_code == 200, f"Frontend returned {fe_res.status_code}"
        assert "<!DOCTYPE html>" in fe_res.text or "<div id=\"root\">" in fe_res.text
        print("PASS: Frontend server reachable at http://localhost:5173/ (HTTP 200)")

    # 2. Backend Health
    with httpx.Client(timeout=10.0) as client:
        health_res = client.get("http://localhost:8000/api/v1/health")
        assert health_res.status_code == 200
        assert health_res.json()["status"] == "ok"
        print("PASS: Backend health check reachable at http://localhost:8000/api/v1/health (HTTP 200)")

    # 3. Authentication - Login
    with httpx.Client(timeout=10.0) as client:
        login_res = client.post(
            "http://localhost:8000/api/v1/auth/login",
            data={"username": "teacher@eduvia.app", "password": "strongpassword123"}
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        tokens = login_res.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        access_token = tokens["access_token"]
        print("PASS: Authenticated login succeeded, issued signed JWT tokens")

    # 4. Authenticated Request - User Profile (/users/me)
    with httpx.Client(timeout=10.0) as client:
        me_res = client.get(
            "http://localhost:8000/api/v1/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert me_res.status_code == 200
        user_data = me_res.json()
        assert user_data["email"] == "teacher@eduvia.app"
        assert user_data["role"] == "teacher"
        print(f"PASS: /users/me returned profile for {user_data['full_name']} (Role: {user_data['role']})")

    # 5. Authenticated Request - List Curricula
    with httpx.Client(timeout=10.0) as client:
        curr_res = client.get(
            "http://localhost:8000/api/v1/curricula",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert curr_res.status_code == 200
        curricula = curr_res.json()
        assert len(curricula) > 0
        curr_id = curricula[0]["id"]
        print(f"PASS: /curricula returned {len(curricula)} curriculum: {curricula[0]['title']['en']}")

    # 6. Authenticated Request - Drill Down Full Hierarchy
    with httpx.Client(timeout=10.0) as client:
        full_curr_res = client.get(
            f"http://localhost:8000/api/v1/curricula/{curr_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert full_curr_res.status_code == 200
        full_curr = full_curr_res.json()
        subjects = full_curr["subjects"]
        assert len(subjects) > 0
        units = subjects[0]["units"]
        assert len(units) > 0
        lessons = units[0]["lessons"]
        assert len(lessons) > 0
        objectives = lessons[0]["learning_objectives"]
        assert len(objectives) == 2
        print(f"PASS: Full hierarchy drill-down verified: {len(subjects)} subjects -> {len(units)} units -> {len(lessons)} lessons -> {len(objectives)} objectives")
        print(f"      Objective 1: '{objectives[0]['title']['en']}' (Difficulty: {objectives[0]['difficulty_level']})")
        print(f"      Objective 2: '{objectives[1]['title']['en']}' (Difficulty: {objectives[1]['difficulty_level']})")

    # 7. Unauthenticated Rejection
    with httpx.Client(timeout=10.0) as client:
        unauth_res = client.get("http://localhost:8000/api/v1/curricula")
        assert unauth_res.status_code == 401
        print("PASS: Unauthenticated request rejected with HTTP 401 Unauthorized")

    # 8. Invalid Token Rejection
    with httpx.Client(timeout=10.0) as client:
        invalid_res = client.get(
            "http://localhost:8000/api/v1/curricula",
            headers={"Authorization": "Bearer invalid.jwt.token"}
        )
        assert invalid_res.status_code == 401
        print("PASS: Invalid token rejected with HTTP 401 Unauthorized")

    # 9. Role Restriction (Teacher cannot create curriculum)
    with httpx.Client(timeout=10.0) as client:
        forbidden_res = client.post(
            "http://localhost:8000/api/v1/curricula",
            json={"title": {"en": "Unauthorized Subject"}},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert forbidden_res.status_code == 403
        print("PASS: Non-admin teacher mutation rejected with HTTP 403 Forbidden")

    print("\nALL 9 LIVE STACK INTEGRATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_live_stack()
