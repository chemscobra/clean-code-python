import os

# you can also use https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.sqlite3")
