import cv2
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class FruitCounter:
    name: str
    count: int
    position_on_screen: List[Tuple[float]] # Subject to change