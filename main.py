from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from controllers.produto_controller import router as produto_router
from controllers.usuario_controller import router as usuario_router

app = FastAPI(title="Sistema de Gerenciamento")


app.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_32_caracteres")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(produto_router, prefix="/produtos")
app.include_router(usuario_router) 

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)