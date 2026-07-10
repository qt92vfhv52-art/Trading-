from dataclasses import dataclass
from enum import Enum

class DCType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"

@dataclass
class DCEvent:

    index: int

    price: float

    threshold: float

    event_type: DCType

    overshoot: float = 0.0

    confirmed: bool = True
