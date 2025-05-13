import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from models.user import User
from database import get_db
from config import settings  # Importando as configurações
from schemas.produto_schema import User as SchemaUser  # Usando o esquema User para validação
from schemas.user_schema import UserCreate, UserLogin  # Importando os esquemas de criação e login de usuário
from schemas.user_schema import UserSchema  # ou UserCreate / UserLogin conforme necessidade

# OAuth2 Password Bearer (para autenticação via token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Função para criar um token JWT com tempo de expiração
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Função para autenticar o usuário (verificar credenciais)
def authenticate_user(db: Session, user_login: UserLogin):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not bcrypt.checkpw(user_login.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Função para obter o usuário atual a partir do token JWT
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificando o token com a chave secreta
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscando o usuário no banco de dados
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Função para verificar se o usuário é um administrador
def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar esta ação",
        )
    return current_user

# Função para criar um novo usuário
def create_user(db: Session, user: UserCreate):
    # Verificar se o usuário já existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Criptografar a senha
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Criar o novo usuário
    db_user = User(username=user.username, email=user.email, password=hashed_password.decode('utf-8'), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
