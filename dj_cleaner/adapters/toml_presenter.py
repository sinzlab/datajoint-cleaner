"""Contains the TOML presenter."""
from ..use_cases.clean import CleanResponseModel


class TOMLPresenter:
    """Presents information about finished executions of use-cases to the command line."""

    @staticmethod
    def clean(response_model: CleanResponseModel) -> None:
        """Present information about a finished execution of the clean use-case to the command line."""
        output_string = f"Deleted {response_model.n_deleted:,d} objects from external storage."
        print(output_string)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
