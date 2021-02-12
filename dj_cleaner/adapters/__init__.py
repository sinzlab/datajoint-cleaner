"""Contains adapters that adapt external interfaces to internal ones."""
from typing import Dict, Type

from .interfaces import AbstractFacadeConfig

FACADE_CONFIGS: Dict[str, Type[AbstractFacadeConfig]] = dict()
