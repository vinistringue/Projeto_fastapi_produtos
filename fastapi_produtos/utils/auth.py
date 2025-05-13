from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verifica se a senha é correta
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Busca o usuário no banco de dados
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
