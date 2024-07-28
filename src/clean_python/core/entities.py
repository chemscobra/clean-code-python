from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BloodborneCharacter(Base):
    """
    SQLAlchemy model for Bloodborne characters.

    Attributes:
        name (str): The name of the character. This is the primary key.
        age (int): The age of the character.
        origin (str): The origin of the character.
        weapon (str): The weapon of the character.
    """

    __tablename__ = "bloodborne_characters"
    name: str = Column(String, primary_key=True, index=True)
    age: int = Column(Integer)
    origin: str = Column(String)
    weapon: str = Column(String)


class BloodborneCharacterModel(BaseModel):
    """
    Pydantic model for Bloodborne characters.

    Attributes:
        name (str): The name of the character.
        age (int): The age of the character.
        origin (str): The origin of the character.
        weapon (str): The weapon of the character.
    """

    name: str = Field(..., description="Name of the hunter")
    age: int = Field(..., description="Age of the hunter")
    origin: str = Field(..., description="Origin of the hunter")
    weapon: str = Field(..., description="Weapon of the hunter")
