from pydantic import BaseModel

class User(BaseModel):
    username: str

    class Config:
        from_attributes = True  # Compatível com o Pydantic V2, substituindo 'orm_mode'
from pydantic import BaseModel

class User(BaseModel):
    username: str

    class Config:
        from_attributes = True  # Compatível com o Pydantic V2, substituindo 'orm_mode'
