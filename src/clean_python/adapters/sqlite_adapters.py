import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.clean_python.core.entities import (
    Base,
    BloodborneCharacter,
    BloodborneCharacterModel,
)
from src.clean_python.core.ports import BloodborneCharacterPort


class SQLiteAdapter(BloodborneCharacterPort):
    """
    SQLite adapter for managing Bloodborne characters in the database.

    Attributes:
        engine (Engine): SQLAlchemy engine for database connection.
        SessionLocal (sessionmaker): SQLAlchemy session factory.
    """

    def __init__(self, db_url: str) -> None:
        """
        Initialize the SQLite adapter with the given database URL.

        Args:
            db_url (str): The database URL.
        """
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        Base.metadata.create_all(bind=self.engine)

    def add_character(self, character: BloodborneCharacterModel) -> None:
        """
        Add a Bloodborne character to the database.

        Args:
            character (BloodborneCharacterModel): The character to add.
        """
        db = self.SessionLocal()
        db_character = BloodborneCharacter(**character.model_dump())
        db.add(db_character)
        db.commit()
        db.close()

    def get_character_by_name(
        self,
        name: str,
    ) -> BloodborneCharacterModel | None:
        """
        Retrieve a Bloodborne character from the database by name.

        Args:
            name (str): The name of the character to retrieve.

        Returns:
            BloodborneCharacterModel | None: The retrieved character,
            or None if not found.
        """
        db = self.SessionLocal()
        character = (
            db.query(BloodborneCharacter)
            .filter(BloodborneCharacter.name == name)
            .first()
        )
        db.close()
        if character:
            return BloodborneCharacterModel(
                name=character.name,
                age=character.age,
                origin=character.origin,
                weapon=character.weapon,
            )
        return None


class SQLiteAdapterWithoutORM(BloodborneCharacterPort):
    """
    Raw SQLite adapter for managing Bloodborne characters in the database.

    Attributes:
        db_path (str): Path to the SQLite database file.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initialize the SQLite adapter with the given database path.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Create the bloodborne_characters table if it does not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bloodborne_characters (
                    name TEXT PRIMARY KEY,
                    age INTEGER,
                    origin TEXT,
                    weapon TEXT
                )
            """)
            conn.commit()

    def add_character(self, character: BloodborneCharacterModel) -> None:
        """
        Add a Bloodborne character to the database.

        Args:
            character (BloodborneCharacterModel): The character to add.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO bloodborne_characters (name, age, origin, weapon)
                VALUES (?, ?, ?, ?)
            """,
                (
                    character.name,
                    character.age,
                    character.origin,
                    character.weapon,
                ),
            )
            conn.commit()

    def get_character_by_name(
        self,
        name: str,
    ) -> BloodborneCharacterModel | None:
        """
        Retrieve a Bloodborne character from the database by name.

        Args:
            name (str): The name of the character to retrieve.

        Returns:
            BloodborneCharacterModel | None: The retrieved character,
            or None if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, age, origin, weapon
                FROM bloodborne_characters
                WHERE name = ?
            """,
                (name,),
            )
            row = cursor.fetchone()
            if row:
                return BloodborneCharacterModel(
                    name=row[0],
                    age=row[1],
                    origin=row[2],
                    weapon=row[3],
                )
            return None
