from pydantic import BaseModel

# Esquema base para criação de uma categoria
class CategoriaBase(BaseModel):
    nome: str

# Esquema para leitura de uma categoria, que inclui o ID
class CategoriaSchema(CategoriaBase):
    id: int

    class Config:
        from_attributes = True  # Permite que o Pydantic trate os modelos do SQLAlchemy
