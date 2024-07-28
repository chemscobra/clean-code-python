from src.clean_python.core.entities import BloodborneCharacterModel
from src.clean_python.core.ports import BloodborneCharacterPort


class BloodborneCharacterUseCase:
    """
    Service class for managing Bloodborne characters.

    Attributes:
        adapter (BloodborneCharacterPort):
        The adapter for storing and retrieving characters.
    """

    def __init__(self, adapter: BloodborneCharacterPort) -> None:
        """
        Initialize the BloodborneCharacterUseCase with the given adapter.

        Args:
            adapter (BloodborneCharacterPort):
            The adapter for storing and retrieving characters.
        """
        self.adapter = adapter

    def add_character(self, character: BloodborneCharacterModel) -> None:
        """
        Add a Bloodborne character to the adapter.

        Args:
            character (BloodborneCharacterModel): The character to add.
        """
        self.adapter.add_character(character)

    def get_character_by_name(
        self,
        name: str,
    ) -> BloodborneCharacterModel | None:
        """
        Retrieve a Bloodborne character from the adapter by name.

        Args:
            name (str): The name of the character to retrieve.

        Returns:
            BloodborneCharacterModel | None: The retrieved character,
            or None if not found.
        """
        return self.adapter.get_character_by_name(name)
