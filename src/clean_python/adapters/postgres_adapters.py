# import psycopg
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from src.clean_python.core.entities import (
#     BloodborneCharacter,
#     BloodborneCharacterModel,
# )
# from src.clean_python.core.ports import BloodborneCharacterPort


# class PostgresAdapter(BloodborneCharacterPort):
#     """
#     PostgreSQL adapter for managing Bloodborne characters in the database using SQLAlchemy ORM.

#     Attributes:
#         engine (Engine): SQLAlchemy engine for database connection.
#         SessionLocal (sessionmaker): SQLAlchemy session factory.
#     """  # noqa: E501

#     def __init__(self, db_url: str) -> None:
#         """
#         Initialize the PostgreSQL adapter with the given database URL.

#         Args:
#             db_url (str): The database URL.
#         """
#         self.engine = create_engine(db_url)
#         self.SessionLocal = sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=self.engine,
#         )
#         # Base.metadata.create_all(bind=self.engine)

#     def add_character(self, character: BloodborneCharacterModel) -> None:
#         """
#         Add a Bloodborne character to the database.

#         Args:
#             character (BloodborneCharacterModel): The character to add.
#         """
#         db = self.SessionLocal()
#         db_character = BloodborneCharacter(**character.model_dump())
#         db.add(db_character)
#         db.commit()
#         db.close()

#     def get_character_by_name(
#         self,
#         name: str,
#     ) -> BloodborneCharacterModel | None:
#         """
#         Retrieve a Bloodborne character from the database by name.

#         Args:
#             name (str): The name of the character to retrieve.

#         Returns:
#             BloodborneCharacterModel | None: The retrieved character, or None if not found.
#         """  # noqa: E501
#         db = self.SessionLocal()
#         character = (
#             db.query(BloodborneCharacter)
#             .filter(BloodborneCharacter.name == name)
#             .first()
#         )
#         db.close()
#         if character:
#             return BloodborneCharacterModel(
#                 name=character.name,
#                 age=character.age,
#                 origin=character.origin,
#                 weapon=character.weapon,
#             )
#         return None


# class PostgresAdapterNoORM(BloodborneCharacterPort):
#     """
#     PostgreSQL adapter for managing Bloodborne characters in the database using raw SQL.

#     Attributes:
#         dsn (str): Data Source Name for connecting to the PostgreSQL database.
#     """

#     def __init__(self, dsn: str) -> None:
#         """
#         Initialize the PostgreSQL adapter with the given DSN.

#         Args:
#             dsn (str): The Data Source Name for connecting to the PostgreSQL database.
#         """
#         self.dsn = dsn
#         self._create_table()

#     def _create_table(self) -> None:
#         """Create the bloodborne_characters table if it does not exist."""
#         with psycopg.connect(self.dsn) as conn, conn.cursor() as cursor:
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS bloodborne_characters (
#                     name TEXT PRIMARY KEY,
#                     age INTEGER,
#                     origin TEXT,
#                     weapon TEXT
#                 )
#             """)
#             conn.commit()

#     def add_character(self, character: BloodborneCharacterModel) -> None:
#         """
#         Add a Bloodborne character to the database.

#         Args:
#             character (BloodborneCharacterModel): The character to add.
#         """
#         with psycopg.connect(self.dsn) as conn, conn.cursor() as cursor:
#             cursor.execute(
#                 """
#                 INSERT INTO bloodborne_characters (name, age, origin, weapon)
#                 VALUES (%s, %s, %s, %s)
#             """,
#                 (
#                     character.name,
#                     character.age,
#                     character.origin,
#                     character.weapon,
#                 ),
#             )
#             conn.commit()

#     def get_character_by_name(self, name: str) -> BloodborneCharacterModel | None:
#         """
#         Retrieve a Bloodborne character from the database by name.

#         Args:
#             name (str): The name of the character to retrieve.

#         Returns:
#             BloodborneCharacterModel | None: The retrieved character, or None if not found.
#         """
#         with psycopg.connect(self.dsn) as conn, conn.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT name, age, origin, weapon
#                 FROM bloodborne_characters
#                 WHERE name = %s
#             """,
#                 (name,),
#             )
#             row = cursor.fetchone()
#             if row:
#                 return BloodborneCharacterModel(
#                     name=row[0], age=row[1], origin=row[2], weapon=row[3]
#                 )
#             return None
