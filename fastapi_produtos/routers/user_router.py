from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserSchema, UserLogin
from auth import create_user, authenticate_user, create_access_token
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# Rota de registro de usuário
@router.post("/register", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

# Rota de login de usuário
@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, user_login=user_login)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users")
def get_users():
    return {"message": "Lista de usuários"}