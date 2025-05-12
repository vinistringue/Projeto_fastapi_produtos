from database import Base, engine
import models  # importa os modelos registrados no __init__.py

print("Criando tabelas no banco de dados...")

# Cria todas as tabelas a partir dos modelos
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
