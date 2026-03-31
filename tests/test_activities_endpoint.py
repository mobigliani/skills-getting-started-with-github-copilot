def test_get_activities_returns_all_seeded_activities(client):
    # Arrange
    expected_activity_names = {
        "Art Studio",
        "Basketball Team",
        "Chess Club",
        "Debate Team",
        "Drama Club",
        "Gym Class",
        "Programming Class",
        "Science Club",
        "Tennis Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json()) == expected_activity_names


def test_get_activities_returns_expected_schema_for_each_activity(client):
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities_payload = response.json()

    # Assert
    assert response.status_code == 200
    for activity in activities_payload.values():
        assert set(activity) == required_keys
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)


def test_get_activities_returns_existing_participants(client):
    # Arrange

    # Act
    response = client.get("/activities")
    activities_payload = response.json()

    # Assert
    assert response.status_code == 200
    assert activities_payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]