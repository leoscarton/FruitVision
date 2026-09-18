from fastapi import APIRouter, HTTPException

from schemas import FruitModel, FruitPackage

router = APIRouter(prefix="/items", tags=["items"])

# Prototype db
_db: dict[int, FruitPackage] = {}
_next_id = 1


# TO DO: Change de function names to english later

@router.get("/", response_model=list[FruitPackage])
def listar():
    return list(_db.values())


@router.get("/{item_id}", response_model=FruitPackage)
def obter(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return _db[item_id]


@router.post("/", response_model=FruitPackage, status_code=201)
def criar(dados: FruitModel):
    global _next_id
    item = FruitPackage(id=_next_id, **dados.model_dump())
    _db[_next_id] = item
    _next_id += 1
    return item