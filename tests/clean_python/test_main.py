import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.clean_python.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_character(sqlite_session: Session) -> None:
    """Test creating a new Bloodborne character."""
    character_data = {
        "name": "Eileen the Crow",
        "age": 30,
        "origin": "Yharnam",
        "weapon": "Blade of Mercy",
    }
    response = client.post("/characters/", json=character_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == character_data["name"]
    assert data["age"] == character_data["age"]
    assert data["origin"] == character_data["origin"]
    assert data["weapon"] == character_data["weapon"]


@pytest.mark.asyncio
async def test_read_character(sqlite_session: Session) -> None:
    """Test retrieving a Bloodborne character by name."""
    character_data = {
        "name": "Lady Maria",
        "age": 28,
        "origin": "Cainhurst",
        "weapon": "Rakuyo",
    }
    # First, create the character
    client.post("/characters/", json=character_data)

    # Then, read the character
    response = client.get("/characters/Lady Maria")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == character_data["name"]
    assert data["age"] == character_data["age"]
    assert data["origin"] == character_data["origin"]
    assert data["weapon"] == character_data["weapon"]


@pytest.mark.asyncio
async def test_read_non_existent_character(sqlite_session: Session) -> None:
    """Test retrieving a non-existent Bloodborne character."""
    response = client.get("/characters/Gehrman the First Hunter")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Character not found"
