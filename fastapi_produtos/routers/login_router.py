from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Autenticação"])

# Carrega chave secreta e algoritmo do .env
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")

# Credenciais fixas para exemplo (em um projeto real use banco de dados e hash)
USUARIO_FAKE = "admin"
SENHA_FAKE = "1234"

@router.post("/login")
def login(usuario: str = Form(...), senha: str = Form(...)):
    if usuario != USUARIO_FAKE or senha != SENHA_FAKE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    
    expiracao = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": usuario,
        "exp": expiracao
    }
    token = jwt.encode(payload, CHAVE_SECRETA, algorithm=ALGORITMO)

    return JSONResponse(content={"access_token": token, "token_type": "bearer"})
