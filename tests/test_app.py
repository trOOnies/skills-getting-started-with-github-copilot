from fastapi import status


def test_root_redirect(client):
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert "Chess Club" in body
    assert "Programming Class" in body


def test_successful_signup_for_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up"


def test_successful_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found"
