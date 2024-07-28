
import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from src.clean_python.adapters.sqlite_adapters import (
    SQLiteAdapter,
)
from src.clean_python.core.entities import BloodborneCharacterModel


@pytest.fixture(scope="module")
def sqlite_adapter(sqlite_engine: Engine) -> SQLiteAdapter:
    """
    Fixture to provide a SQLiteAdapter instance for tests.

    Args:
        sqlite_engine (Engine): The SQLAlchemy engine fixture for SQLite.

    Returns:
        SQLiteAdapter: Instance of SQLiteAdapter.
    """
    return SQLiteAdapter(db_url=str(sqlite_engine.url))


def test_add_and_get_character_orm(
    sqlite_adapter: SQLiteAdapter, sqlite_session: Session
) -> None:
    """
    Test adding and retrieving a Bloodborne character using SQLAlchemy ORM.

    Args:
        sqlite_adapter (SQLiteAdapter): The SQLiteAdapter instance.
        session (Session): The SQLAlchemy session fixture.
    """
    character = BloodborneCharacterModel(
        name="Hunter2", age=30, origin="Yharnam", weapon="Saw Cleaver"
    )
    sqlite_adapter.add_character(character)

    retrieved_character = sqlite_adapter.get_character_by_name("Hunter2")
    assert retrieved_character is not None
    assert retrieved_character.name == "Hunter2"
    assert retrieved_character.age == 30
    assert retrieved_character.origin == "Yharnam"
    assert retrieved_character.weapon == "Saw Cleaver"


def test_get_non_existent_character_orm(sqlite_adapter: SQLiteAdapter) -> None:
    """
    Test retrieving a non-existent Bloodborne character using SQLAlchemy ORM.

    Args:
        sqlite_adapter (SQLiteAdapter): The SQLiteAdapter instance.
    """
    retrieved_character = sqlite_adapter.get_character_by_name("NonExistent")
    assert retrieved_character is None
