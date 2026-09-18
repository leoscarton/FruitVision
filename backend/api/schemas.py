from pydantic import BaseModel

class FruitModel(BaseModel):
    name: str
    count: int
    position_on_screen: list[tuple[float, float]]

class FruitPackage(FruitModel):
    id: int