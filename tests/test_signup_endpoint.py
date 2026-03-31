from src.app import activities


def test_signup_adds_participant_and_returns_success_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    activities[activity_name]["participants"] = [
        f"student{index}@mergington.edu" for index in range(activities[activity_name]["max_participants"])
    ]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "late.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


def test_signup_requires_email_query_parameter(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_signup_rejects_empty_email(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": ""},
    )

    # Assert
    assert response.status_code == 422


def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "not-an-email"},
    )

    # Assert
    assert response.status_code == 422


def test_signup_allows_student_to_rejoin_after_unregistration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "returning.student@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_succeeds_after_capacity_is_freed(client):
    # Arrange
    activity_name = "Chess Club"
    activities[activity_name]["participants"] = [
        f"student{index}@mergington.edu" for index in range(activities[activity_name]["max_participants"])
    ]
    removed_email = activities[activity_name]["participants"][0]
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": removed_email},
    )
    new_email = "new.capacity@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert new_email in activities[activity_name]["participants"]