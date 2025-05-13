from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: str

@router.post("/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    # Lógica para solicitar o reset de senha
    return {"message": f"Senha de {request.email} resetada com sucesso!"}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    # Lógica para resetar a senha usando o token
    return {"message": "Senha alterada com sucesso!"}
