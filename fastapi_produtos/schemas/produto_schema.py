from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria_id: int

class ProdutoSchema(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
        
class User(BaseModel):
    username: str