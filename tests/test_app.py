def test_home(client):

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_health(client):

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate_demo_plan(client):

    response = client.post(

        "/generate-workout",

        data={

            "user_id": "TEST001",

            "name": "Demo User",

            "age": "20",

            "weight": "60",

            "goal": "general wellness",

            "intensity": "medium",

            "experience_level": "beginner"

        }

    )


    assert response.status_code == 200

    assert "DAY 1" in response.text

    assert "Nutrition" in response.text


def test_api_get_user(client):

    client.post(

        "/generate-workout",

        data={

            "user_id": "TEST002",

            "name": "API User",

            "age": "21",

            "weight": "62",

            "goal": "muscle gain",

            "intensity": "low",

            "experience_level": "beginner"

        }

    )


    response = client.get(
        "/api/users/TEST002"
    )


    assert response.status_code == 200

    assert (
        response.json()["user_id"]
        == "TEST002"
    )


def test_admin_protection(client):

    response = client.get(
        "/view-all-users"
    )

    assert response.status_code == 403


    response = client.get(
        "/view-all-users?key=test-admin"
    )

    assert response.status_code == 200