import os
from collections.abc import Generator
from typing import Any

import pytest

from src.clean_python.adapters.sqlite_adapters import (
    SQLiteAdapterWithoutORM,
)
from src.clean_python.core.entities import BloodborneCharacterModel


@pytest.fixture(scope="module")
def sqlite_adapter_no_orm() -> Generator[SQLiteAdapterWithoutORM, Any, Any]:
    """
    Fixture to provide a SQLiteAdapterWithoutORM instance for tests.

    Returns:
        SQLiteAdapterWithoutORM: Instance of SQLiteAdapterWithoutORM.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    db_path = DATABASE_URL.split("///")[-1]  # Extract the file path from the URL
    adapter = SQLiteAdapterWithoutORM(db_path=db_path)
    yield adapter


def test_add_and_get_character_no_orm(
    sqlite_adapter_no_orm: SQLiteAdapterWithoutORM,
) -> None:
    """
    Test adding and retrieving a Bloodborne character using raw SQL with sqlite3.

    Args:
        sqlite_adapter_no_orm (SQLiteAdapterWithoutORM): The SQLiteAdapterWithoutORM instance.
    """
    character = BloodborneCharacterModel(
        name="Hunter", age=30, origin="Yharnam", weapon="Saw Cleaver"
    )
    sqlite_adapter_no_orm.add_character(character)

    retrieved_character = sqlite_adapter_no_orm.get_character_by_name("Hunter")
    assert retrieved_character is not None
    assert retrieved_character.name == "Hunter"
    assert retrieved_character.age == 30
    assert retrieved_character.origin == "Yharnam"
    assert retrieved_character.weapon == "Saw Cleaver"


def test_get_non_existent_character_no_orm(
    sqlite_adapter_no_orm: SQLiteAdapterWithoutORM,
) -> None:
    """
    Test retrieving a non-existent Bloodborne character using raw SQL with sqlite3.

    Args:
        sqlite_adapter_no_orm (SQLiteAdapterWithoutORM): The SQLiteAdapterWithoutORM instance.
    """
    retrieved_character = sqlite_adapter_no_orm.get_character_by_name("NonExistent")
    assert retrieved_character is None
