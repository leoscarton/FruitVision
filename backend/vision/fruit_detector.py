import cv2
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class FruitCounter:
    name: str
    count: int
    position_on_screen: List[Tuple[float, float]] = field(default_factory=list) # Subject to change

    def __post_init__(self):
        for p in self.position_on_screen:
            if len(p) != 2:
                raise ValueError(f"Each tuple must have exactly 2 elements, {p} has {len(p)}")
            elif (p[0] < 0.0) or (p[1] < 0.0):
                raise ValueError(f"Screen coordinates cannot be negative")

        if self.count < 0:
            raise ValueError("Fruit count cannot be negative")

    def fruit_detected(self):
        return (self.count > 0)

    def update_count(self, new_count):
        if new_count < 0:
            raise ValueError("Fruit count cannot be negative")
        else:
            self.count = new_count

    def add_fruit_position(self, fruit_pos:tuple):
        if len(fruit_pos) != 2:
            raise ValueError(f"Each tuple must have exactly 2 elements, {fruit_pos} has {len(fruit_pos)}")
        elif fruit_pos[0] < 0.0 or fruit_pos[1] < 0.0:
            raise ValueError(f"Screen coordinates cannot be negative")
        else:
            self.position_on_screen.append(fruit_pos)