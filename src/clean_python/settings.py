import os

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.sqlite3")
