"""Contains entrypoints to the package."""
import sys

from dj_cleaner import toml_cli


def toml_cli_entry() -> None:
    """Run the TOML command line interface."""
    toml_cli.clean(sys.argv[1:])


if __name__ == "__main__":
    toml_cli_entry()
