from fastapi import FastAPI
from routers.produto_router import router as produto_router
from routers.categoria_router import router as categoria_router
from database import criar_bd
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user_router
from routers.user_router import router as user_router  # Correção: Importando a variável user_router

# Instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Produtos e Categorias",
    description="Projeto com FastAPI, MySQL e autenticação JWT",
    version="1.0.0"
)

# Configuração de CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens, pode ser ajustado para segurança
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Inclusão dos routers
app.include_router(auth.router)         # Rota de autenticação
app.include_router(categoria_router)    # Rota de categorias
app.include_router(produto_router)      # Rota de produtos
app.include_router(user_router)         # Correção: Incluindo o router de usuários

# Rota de saúde (verificação do status da aplicação)
@app.get("/health")
def health_check():
    return {"status": "Aplicação rodando corretamente"}

# Rota para a raiz ("/")
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Produtos e Categorias!"}

# Criação das tabelas no banco de dados (executado somente se for main)
if __name__ == "__main__":
    criar_bd()
