from typing import NamedTuple
from dataclasses import dataclass


@dataclass
class FieldDefinition:
    field: str
    type: str
    not_null: bool
    description: str