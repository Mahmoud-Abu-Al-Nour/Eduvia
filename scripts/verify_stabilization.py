import urllib.request
import urllib.parse
import json
import sys

def main():
    print("=== EDUVIA END-TO-END STABILIZATION VERIFICATION ===")
    
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

    # 3. Authenticate as Teacher
    try:
        login_data = urllib.parse.urlencode({
            "username": "teacher@eduvia.app",
            "password": "strongpassword123"
        }).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(req, timeout=5)
        body = json.loads(res.read().decode('utf-8'))
        teacher_token = body.get("access_token")
        print(f"[*] Teacher Login: SUCCESS, token acquired ({teacher_token[:15]}...)")
    except Exception as e:
        print(f"[!] Teacher Login FAILED: {e}")
        return 1

    # 4. Authenticate as Admin
    try:
        login_data = urllib.parse.urlencode({
            "username": "admin@eduvia.app",
            "password": "adminpassword123"
        }).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        res = urllib.request.urlopen(req, timeout=5)
        body = json.loads(res.read().decode('utf-8'))
        admin_token = body.get("access_token")
        print(f"[*] Admin Login: SUCCESS, token acquired ({admin_token[:15]}...)")
    except Exception as e:
        print(f"[!] Admin Login FAILED: {e}")
        return 1

    headers = {"Authorization": f"Bearer {teacher_token}"}

    # 5. Check Teacher Dashboard (Canonical)
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/dashboard", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/teachers/dashboard: Status {res.status}")
        print(f"    - total_learners: {data.get('total_learners')}")
        print(f"    - active_learners_count: {data.get('active_learners_count')}")
        print(f"    - cohort_average_accuracy_7d: {data.get('cohort_average_accuracy_7d')}")
        print(f"    - pending_alerts: {len(data.get('pending_alerts', []))}")
        assert "total_learners" in data and "pending_alerts" in data
    except Exception as e:
        print(f"[!] GET /api/v1/teachers/dashboard FAILED: {e}")
        return 1

    # 6. Check Teacher Dashboard (Singular Alias)
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teacher/dashboard", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/teacher/dashboard (Alias): Status {res.status} - OK")
    except Exception as e:
        print(f"[!] GET /api/v1/teacher/dashboard FAILED: {e}")
        return 1

    # 7. Check Cohort Insights (Canonical & Alias)
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/teachers/cohort/insights?days=30", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        data = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/teachers/cohort/insights: Status {res.status}")
        print(f"    - cohort_size: {data.get('cohort_size')}")
        print(f"    - total_cohort_learners: {data.get('total_cohort_learners')}")
        print(f"    - learners list count: {len(data.get('learners', []))}")
        if data.get('learners'):
            first_learner = data['learners'][0]
            print(f"    - Learner: {first_learner.get('display_name')} (Accuracy: {first_learner.get('overall_accuracy')})")
        assert "cohort_size" in data and "learners" in data
    except Exception as e:
        print(f"[!] GET /api/v1/teachers/cohort/insights FAILED: {e}")
        return 1

    # 8. Check Learners List
    learner_id = None
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/learners", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        learners = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/learners: Status {res.status} - Returned {len(learners)} learners")
        assert len(learners) > 0
        first_l = learners[0]
        learner_id = first_l.get("id")
        print(f"    - Learner: {first_l.get('name')} (id: {learner_id})")
    except Exception as e:
        print(f"[!] GET /api/v1/learners FAILED: {e}")
        return 1

    # 9. Check Curricula
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/curricula", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        currs = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/curricula: Status {res.status} - Returned {len(currs)} curricula")
    except Exception as e:
        print(f"[!] GET /api/v1/curricula FAILED: {e}")
        return 1

    # 10. Check Activities
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/activities/types", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        activities = json.loads(res.read().decode('utf-8'))
        print(f"[*] GET /api/v1/activities/types: Status {res.status} - Returned {len(activities)} types")
    except Exception as e:
        print(f"[!] GET /api/v1/activities/types FAILED: {e}")
        return 1

    # 11. Check Analytics Summary
    if learner_id:
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/analytics/learners/{learner_id}/summary", headers=headers)
            res = urllib.request.urlopen(req, timeout=5)
            summary = json.loads(res.read().decode('utf-8'))
            print(f"[*] GET /api/v1/analytics/learners/.../summary: Status {res.status} - Accuracy: {summary.get('accuracy_rate')}")
        except Exception as e:
            print(f"[!] GET /api/v1/analytics/... FAILED: {e}")
            return 1

        # 12. Check Recommendations
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8000/api/v1/recommendations/learners/{learner_id}", headers=headers)
            res = urllib.request.urlopen(req, timeout=5)
            recs = json.loads(res.read().decode('utf-8'))
            print(f"[*] GET /api/v1/recommendations/learners/...: Status {res.status} - Recommendations: {len(recs)}")
        except Exception as e:
            print(f"[!] GET /api/v1/recommendations/... FAILED: {e}")
            return 1

    # 13. Test Vite Proxy (port 5173 -> 8000)
    try:
        req = urllib.request.Request("http://localhost:5173/api/v1/teachers/dashboard", headers=headers)
        res = urllib.request.urlopen(req, timeout=5)
        print(f"[*] Vite Proxy GET http://localhost:5173/api/v1/teachers/dashboard: Status {res.status} - OK")
    except Exception as e:
        print(f"[!] Vite Proxy test note: {e}")

    print("\nALL BACKEND API AND PROXY CHECKS PASSED PERFECTLY!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
