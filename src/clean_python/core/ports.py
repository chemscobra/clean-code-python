from abc import ABC, abstractmethod

from .entities import BloodborneCharacterModel


class BloodborneCharacterPort(ABC):
    """Abstract base class for a repository managing Bloodborne characters."""

    @abstractmethod
    def add_character(self, character: BloodborneCharacterModel) -> None:
        """
        Add a Bloodborne character to the repository.

        Args:
            character (BloodborneCharacterModel): The character to add.
        """
        ...

    @abstractmethod
    def get_character_by_name(
        self,
        name: str,
    ) -> BloodborneCharacterModel | None:
        """
        Retrieve a Bloodborne character from the repository by name.

        Args:
            name (str): The name of the character to retrieve.

        Returns:
            BloodborneCharacterModel | None: The retrieved character,
            or None if not found.
        """
        ...
