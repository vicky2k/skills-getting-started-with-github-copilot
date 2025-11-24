from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_reflect():
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure email not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Cleanup
    activities[activity]["participants"].remove(email)


def test_unregister_endpoint():
    activity = "Programming Class"
    email = "temp.user@example.com"

    # Ensure present by signing up first
    if email not in activities[activity]["participants"]:
        resp = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert resp.status_code == 200

    # Now unregister
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
