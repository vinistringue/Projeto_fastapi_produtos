from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = "mysql+pymysql://usuario:senha@localhost/nome_do_banco"  # Atualize aqui

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para criar as tabelas no banco
def criar_bd():
    from models import produto_model, categoria_model  # Certifique-se que os models estão sendo importados
    Base.metadata.create_all(bind=engine)

# Dependência para injetar sessão do banco no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
