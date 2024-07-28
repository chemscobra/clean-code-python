import os
from collections.abc import Generator
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """
    Fixture to create a SQLite engine for the session.

    Returns:
        Engine: SQLAlchemy Engine object for SQLite.
    """
    # Load environment variables from .env.test
    env_path = Path(__file__).parent / "clean_python/.env.test"
    load_dotenv(dotenv_path=env_path)


# region SQLite Stuff


@pytest.fixture(scope="session")
def sqlite_alembic_config() -> Config:
    """
    Fixture to provide the Alembic configuration.

    Returns:
        Config: Alembic configuration object.
    """
    alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    return Config(str(alembic_ini_path))


@pytest.fixture(scope="session")
def sqlite_engine() -> Generator[Engine, None, None]:
    """
    Fixture to create a SQLite engine for the session.

    Returns:
        Engine: SQLAlchemy Engine object for SQLite.
    """
    db_url = os.getenv("DATABASE_URL")
    yield create_engine(db_url)
    # Cleanup: Remove the SQLite database file
    db_path = db_url.split("///")[-1]
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="session")
def setup_sqlite_database(
    sqlite_engine: Engine, sqlite_alembic_config: Config
) -> Generator[None, None, None]:
    """
    Fixture to set up the database using Alembic migrations.

    Args:
        engine (Engine): The SQLAlchemy Engine object.
        sqlite_alembic_config (Config): The Alembic configuration object.
    """
    sqlite_alembic_config.set_main_option("sqlalchemy.url", str(sqlite_engine.url))
    command.upgrade(sqlite_alembic_config, "head")
    yield
    command.downgrade(sqlite_alembic_config, "base")


@pytest.fixture(scope="session")
def sqlite_session(sqlite_engine: Engine) -> Generator[Session, None, None]:
    """
    Fixture to provide a SQLAlchemy session for tests.

    Args:
        engine (Engine): The SQLAlchemy Engine object.
        setup_database: The setup_database fixture.

    Returns:
        Session: SQLAlchemy Session object.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
    session = SessionLocal()
    yield session
    session.close()
