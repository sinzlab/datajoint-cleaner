"""Contains the TOML presenter."""
from ..use_cases.clean import CleanResponseModel


class TOMLPresenter:
    """Presents information about finished executions of use-cases to the command line."""

    def clean(self, response_model: CleanResponseModel) -> None:
        """Present information about a finished execution of the clean use-case to the command line."""

    def __repr__(self) -> str:
        """Return a string representation of the object."""
