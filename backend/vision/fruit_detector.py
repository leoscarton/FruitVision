import cv2
from dataclasses import dataclass, field, asdict
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

    def __repr__(self):
        pos_repr = f""
        for id, p in enumerate(self.position_on_screen):
            pos_repr += f"{id+1}: "
            pos_repr += str(p)
            pos_repr += "\n"    

        return f"Name: {self.name}\nCount: {self.count}\nPositions on Screen:\n{pos_repr}"

    def fruit_detected(self):
        return (self.count > 0)

    def update_count(self, new_count):
        if not isinstance(new_count, int):
            raise TypeError("Count must be integer")
        if new_count < 0:
            raise ValueError("Fruit count cannot be negative")
        else:
            self.count = new_count

    def add_fruit_position(self, fruit_pos:tuple):
        if not isinstance(fruit_pos, tuple):
            raise TypeError(f"Fruit coordinates must be a tuple, instead got {type(fruit_pos)}")
        
        if len(fruit_pos) != 2:
            raise ValueError(f"Each tuple must have exactly 2 elements, {fruit_pos} has {len(fruit_pos)}")

        if not ((isinstance(fruit_pos[0], float) or isinstance(fruit_pos[0], int)) and (isinstance(fruit_pos[1], float) or isinstance(fruit_pos[1], int))):
            raise TypeError(f"Fruit position must be of type float or int, instead got ({type(fruit_pos[0]), type(fruit_pos[1])})")
        
        if fruit_pos[0] < 0.0 or fruit_pos[1] < 0.0:
            raise ValueError(f"Screen coordinates cannot be negative")
        else:
            self.position_on_screen.append(fruit_pos)


class FruitCountManager:
    def __init__(self):
        self.fruit_counters = []
        self.number_of_counters = 0

    def find_fruit(self, fruit_name:str):
        for fruit in self.fruit_counters:
            if fruit.name == fruit_name:
                return fruit

        return None

    def add_fruit(self, fruit_cnt:FruitCounter):
        if self.find_fruit(fruit_cnt.name) is not None:
            raise ValueError(f"Fruit {fruit_cnt.name} already present in list")
            
        self.fruit_counters.append(fruit_cnt)
        self.number_of_counters += 1

    def update_fruit_counter(self, fruit_name:str, new_count:int):
        fruit = self.find_fruit(fruit_name)
        fruit.update_count(new_count)

    def send_dict(self) -> dict:
        d = {fruit.name : asdict(fruit) for fruit in self.fruit_counters}
        return d