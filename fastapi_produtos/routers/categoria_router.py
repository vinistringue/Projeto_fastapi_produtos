from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.categoria_model import Categoria
from schemas.categoria_schema import CategoriaBase, CategoriaSchema
from auth import get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorias"])

# Função para criar categoria
@router.post("/", response_model=CategoriaSchema, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoriaBase, db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    # Verificar se a categoria já existe antes de criar
    categoria_existente = db.query(Categoria).filter(Categoria.nome == categoria.nome).first()
    if categoria_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria já existente")
    
    # Criar nova categoria
    nova_categoria = Categoria(**categoria.dict())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    
    return nova_categoria

# Função para listar todas as categorias
@router.get("/", response_model=List[CategoriaSchema])
def listar_categorias(db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    categorias = db.query(Categoria).all()
    if not categorias:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma categoria encontrada")
    return categorias

# Função para buscar uma categoria específica pelo ID
@router.get("/{categoria_id}", response_model=CategoriaSchema)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return categoria

# Função para atualizar uma categoria
@router.put("/{categoria_id}", response_model=CategoriaSchema)
def atualizar_categoria(categoria_id: int, dados: CategoriaBase, db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    
    # Atualizando os campos da categoria
    for campo, valor in dados.dict().items():
        setattr(categoria, campo, valor)
    
    db.commit()
    db.refresh(categoria)
    
    return categoria

# Função para deletar uma categoria
@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    
    db.delete(categoria)
    db.commit()
    
    return {"mensagem": "Categoria deletada com sucesso"}
