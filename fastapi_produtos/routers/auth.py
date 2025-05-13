from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta, datetime
import jwt
from models.user import User
 # Ajuste conforme seu modelo de User
from schemas import Token, TokenData
  # Ajuste conforme seu esquema de Token
from config import SECRET_KEY, ALGORITHM  # Ajuste conforme sua chave secreta
from utils.auth import get_user, verify_password



router = APIRouter()

# Função para criar o access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para criar o refresh token
def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):  # Expiração mais longa
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint de login que gera tanto o access quanto o refresh token
@router.post("/auth/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)  # Ajuste conforme sua lógica para buscar o usuário
    if user is None or not verify_password(form_data.password, user.password):  # Ajuste para sua validação
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(hours=1)  # Expiração do access token
    refresh_token_expires = timedelta(days=7)  # Expiração do refresh token

    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Endpoint para renovação de token
@router.post("/auth/refresh-token", response_model=Token)
def refresh_access_token(refresh_token: str):
    try:
        # Decodificar o refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        user = get_user(username)  # Ajuste conforme sua lógica de obtenção do usuário
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Gerar um novo access token
        new_access_token = create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Refresh token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
