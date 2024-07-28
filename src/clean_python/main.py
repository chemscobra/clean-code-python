from fastapi import FastAPI, HTTPException

from src.clean_python import settings
from src.clean_python.adapters.sqlite_adapters import SQLiteAdapter
from src.clean_python.core.entities import BloodborneCharacterModel
from src.clean_python.core.use_cases import BloodborneCharacterUseCase

app = FastAPI()

repository = SQLiteAdapter(settings.DATABASE_URL)
service = BloodborneCharacterUseCase(repository)


@app.post("/characters/", response_model=BloodborneCharacterModel)
async def create_character(
    character: BloodborneCharacterModel,
) -> BloodborneCharacterModel:
    """
    Create a new Bloodborne character.

    Args:
        character (BloodborneCharacterModel): The character data.

    Returns:
        BloodborneCharacterModel: The created character.
    """
    service.add_character(character)
    return character


@app.get("/characters/{name}", response_model=BloodborneCharacterModel)
async def read_character(name: str) -> BloodborneCharacterModel:
    """
    Retrieve a Bloodborne character by name.

    Args:
        name (str): The name of the character to retrieve.

    Returns:
        BloodborneCharacterModel: The retrieved character.

    Raises:
        HTTPException: If the character is not found.
    """
    character = service.get_character_by_name(name)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
