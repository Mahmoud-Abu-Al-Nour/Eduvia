import urllib.request
import urllib.parse
import json
import sys

def login(email, password):
    login_data = urllib.parse.urlencode({
        "username": email,
        "password": password
    }).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    res = urllib.request.urlopen(req, timeout=5)
    body = json.loads(res.read().decode('utf-8'))
    return body.get("access_token")

def main():
    print("=== EDUVIA END-TO-END TEST SEEDING & STABILIZATION VERIFICATION ===")
    
    # 1. Frontend check
    try:
        req = urllib.request.urlopen("http://localhost:5173", timeout=5)
        content = req.read().decode('utf-8', errors='ignore')
        print(f"[*] Frontend http://localhost:5173: Status {req.status} - OK")
        assert "Eduvia" in content or "vite" in content
    except Exception as e:
        print(f"[!] Frontend error: {e}")
        return 1

    # 2. Backend docs check
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=5)
        print(f"[*] Backend http://127.0.0.1:8000/docs: Status {req.status} - OK")
    except Exception as e:
        print(f"[!] Backend docs error: {e}")
        return 1

    # 3. Authenticate as Teacher A (Cohort A), Teacher B (Cohort B), and Admin
    teacher_a_token = login("teacher@eduvia.app", "strongpassword123")
    print(f"[*] Teacher A (Cohort A) Login: SUCCESS")

    teacher_b_token = login("teacher.cohortb@eduvia.local", "strongpassword123")
    print(f"[*] Teacher B (Cohort B) Login: SUCCESS")

    admin_token = login("admin@eduvia.app", "adminpassword123")
    print(f"[*] Admin Login: SUCCESS")

    headers_a = {"Authorization": f"Bearer {teacher_a_token}"}
    headers_b = {"Authorization": f"Bearer {teacher_b_token}"}
    headers_admin = {"Authorization": f"Bearer {admin_token}"}

    # 4. Verify Cohort A Dashboard & Insights
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/dashboard", headers=headers_a)
    res = urllib.request.urlopen(req, timeout=5)
    dash_a = json.loads(res.read().decode('utf-8'))
    print(f"[*] Teacher A Dashboard: Total Learners = {dash_a.get('total_learners')}, Active 7d = {dash_a.get('active_learners_7d')}, 7d Acc = {dash_a.get('cohort_average_accuracy_7d')}, Alerts = {dash_a.get('active_alerts_count')}")
    assert dash_a.get('total_learners') == 11, f"Expected 11 learners for Cohort A, got {dash_a.get('total_learners')}"

    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/cohort/insights?days=30", headers=headers_a)
    res = urllib.request.urlopen(req, timeout=5)
    insights_a = json.loads(res.read().decode('utf-8'))
    print(f"[*] Cohort A Insights: Size = {insights_a.get('cohort_size')}, Avg Acc = {insights_a.get('average_accuracy')}, Mastery = {insights_a.get('mastery_distribution')}")
    assert insights_a.get('average_accuracy') >= 0.85, "Cohort A should be high-performing"

    # 5. Verify Cohort B Dashboard & Insights
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/dashboard", headers=headers_b)
    res = urllib.request.urlopen(req, timeout=5)
    dash_b = json.loads(res.read().decode('utf-8'))
    print(f"[*] Teacher B Dashboard: Total Learners = {dash_b.get('total_learners')}, Active 7d = {dash_b.get('active_learners_7d')}, 7d Acc = {dash_b.get('cohort_average_accuracy_7d')}, Alerts = {dash_b.get('active_alerts_count')}")
    assert dash_b.get('total_learners') == 10, f"Expected 10 learners for Cohort B, got {dash_b.get('total_learners')}"

    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/cohort/insights?days=30", headers=headers_b)
    res = urllib.request.urlopen(req, timeout=5)
    insights_b = json.loads(res.read().decode('utf-8'))
    print(f"[*] Cohort B Insights: Size = {insights_b.get('cohort_size')}, Avg Acc = {insights_b.get('average_accuracy')}, Mastery = {insights_b.get('mastery_distribution')}")
    assert insights_b.get('average_accuracy') < 0.70, "Cohort B should have more struggling students"

    # 6. Verify Admin sees all 21 learners
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/learners", headers=headers_admin)
    res = urllib.request.urlopen(req, timeout=5)
    all_learners = json.loads(res.read().decode('utf-8'))
    print(f"[*] Admin GET /api/v1/learners: Total = {len(all_learners)} learners (20 test students + Tariq)")
    assert len(all_learners) >= 21, f"Expected at least 21 learners for admin, got {len(all_learners)}"

    # 7. Verify Specific Scenario Students
    learner_map = {l['name']: l for l in all_learners}

    # Scenario A: Test Student - Excellent
    student_exc = learner_map.get("Test Student - Excellent")
    assert student_exc is not None, "Test Student - Excellent missing"
    exc_id = student_exc['id']

    req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/recommendations/learners/{exc_id}", headers=headers_admin)
    res = urllib.request.urlopen(req, timeout=5)
    rec_exc = json.loads(res.read().decode('utf-8'))
    print(f"[*] Scenario 'Excellent' Recommendation: Activity={rec_exc.get('recommended_activity_type')}, Strategy={rec_exc.get('recommended_strategy')}, Tier={rec_exc.get('scaffolding_tier')}")
    assert rec_exc.get('recommended_strategy') == "gradual_difficulty", "Excellent student should get gradual difficulty"

    # Scenario B: Test Student - Struggling
    student_str = learner_map.get("Test Student - Struggling")
    assert student_str is not None, "Test Student - Struggling missing"
    str_id = student_str['id']

    req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/recommendations/learners/{str_id}", headers=headers_admin)
    res = urllib.request.urlopen(req, timeout=5)
    rec_str = json.loads(res.read().decode('utf-8'))
    print(f"[*] Scenario 'Struggling' Recommendation: Activity={rec_str.get('recommended_activity_type')}, Strategy={rec_str.get('recommended_strategy')}, Tier={rec_str.get('scaffolding_tier')}")
    assert rec_str.get('recommended_strategy') == "demonstration", "Struggling student should get demonstration strategy"
    assert rec_str.get('scaffolding_tier') == 2, "Struggling student should get Tier 2 scaffolding"

    # Scenario C: Test Student - At Risk
    student_risk = learner_map.get("Test Student - At Risk")
    assert student_risk is not None, "Test Student - At Risk missing"
    risk_id = student_risk['id']

    req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/teachers/dashboard", headers=headers_b)
    res = urllib.request.urlopen(req, timeout=5)
    dash_b = json.loads(res.read().decode('utf-8'))
    alerts = dash_b.get("pending_alerts", [])
    risk_alert = next((a for a in alerts if "At Risk" in a.get("learner_display_name", "")), None)
    print(f"[*] Scenario 'At Risk' Alert detected: {risk_alert.get('message') if risk_alert else 'None'}")
    assert risk_alert is not None, "At Risk alert should be present in Cohort B alerts"

    # 8. Check Curriculum Endpoint
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/curricula", headers=headers_admin)
    res = urllib.request.urlopen(req, timeout=5)
    currs = json.loads(res.read().decode('utf-8'))
    print(f"[*] GET /api/v1/curricula: Status {res.status} - Returned {len(currs)} curricula")
    assert len(currs) > 0

    # 9. Check Activity Types Endpoint
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/activities/types", headers=headers_admin)
    res = urllib.request.urlopen(req, timeout=5)
    act_types = json.loads(res.read().decode('utf-8'))
    print(f"[*] GET /api/v1/activities/types: Status {res.status} - Returned {len(act_types)} types")
    assert len(act_types) > 0

    # 10. Check IEP Report Endpoint for Learner
    req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/teachers/learners/{exc_id}/iep-report?days=30", headers=headers_a)
    res = urllib.request.urlopen(req, timeout=5)
    iep = json.loads(res.read().decode('utf-8'))
    print(f"[*] IEP Report for '{student_exc['name']}': Accuracy = {iep.get('overall_accuracy')}, Modality = {iep.get('communication_preference')}")
    assert iep.get('learner_display_name') == "Test Student - Excellent"

    # 11. Vite Proxy Test
    req = urllib.request.Request("http://localhost:5173/api/v1/teachers/dashboard", headers=headers_a)
    res = urllib.request.urlopen(req, timeout=5)
    print(f"[*] Vite Reverse Proxy: Status {res.status} - OK")

    print("\n=======================================================")
    print("ALL 11 TEST SUITES PASSED! TEST DATA SEEDING VERIFIED!")
    print("=======================================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
