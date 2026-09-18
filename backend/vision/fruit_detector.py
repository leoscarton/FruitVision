import cv2
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class FruitCounter:
    name: str
    count: int
    #is_on_screen: bool = False
    position_on_screen: List[Tuple[float, float]] = field(default_factory=list) # Subject to change

    def __post_init__(self):
        for p in self.position_on_screen:
            if len(p) != 2:
                raise ValueError(f"Each tuple must have exactly 2 elements, {p} has {len(p)}")

        if self.count < 0:
            raise ValueError("Fruit count cannot be negative")

    def fruit_detected(self):
        return (self.count > 0)