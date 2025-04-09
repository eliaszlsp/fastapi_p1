from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from routes.produtos_routes import router as produto_router
from routes.usuario_routes import router as usuario_router

app = FastAPI(title="Sistema de Gerenciamento")



templates = Jinja2Templates(directory="templates")

app.include_router(produto_router, prefix="/produtos")
app.include_router(usuario_router, prefix="/usuarios")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
