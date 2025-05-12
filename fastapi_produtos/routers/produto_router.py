from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.produto_model import Produto
from schemas.produto_schema import ProdutoBase, ProdutoSchema
from auth import get_current_user, get_current_admin_user  # ✅ Importações corretas
from sqlalchemy import or_

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Função para criar um novo produto
@router.post("/", response_model=ProdutoSchema, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoBase,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)  # ✅ Validação do usuário autenticado
):
    # Verificar se o produto já existe antes de criar
    produto_existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
    if produto_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produto já existente")
    
    # Criar novo produto
    novo_produto = Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    return novo_produto

# Função para listar todos os produtos com filtros e paginação
@router.get("/", response_model=List[ProdutoSchema])
def listar_produtos(
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
    categoria_id: Optional[int] = None,
    min_preco: Optional[float] = None,
    max_preco: Optional[float] = None,
    skip: int = 0,
    limit: int = 10
):
    # Aplicar filtros se passados
    query = db.query(Produto)
    
    if categoria_id:
        query = query.filter(Produto.categoria_id == categoria_id)
    if min_preco:
        query = query.filter(Produto.preco >= min_preco)
    if max_preco:
        query = query.filter(Produto.preco <= max_preco)
    
    # Paginação
    produtos = query.offset(skip).limit(limit).all()
    if not produtos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto encontrado")
    
    return produtos

# Função para buscar um produto específico pelo ID
@router.get("/{produto_id}", response_model=ProdutoSchema)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

# Função para atualizar um produto
@router.put("/{produto_id}", response_model=ProdutoSchema)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoBase,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    # Verificando se o usuário autenticado é o dono do produto
    if produto.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para editar este produto")
    
    # Atualizando os campos do produto
    for campo, valor in dados.dict().items():
        setattr(produto, campo, valor)
    
    db.commit()
    db.refresh(produto)
    
    return produto

# Função para deletar um produto - Substituída para verificar se o usuário é admin
@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_admin_user)  # Verificação se o usuário é admin
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    db.delete(produto)
    db.commit()
    
    return {"mensagem": "Produto deletado com sucesso"}
