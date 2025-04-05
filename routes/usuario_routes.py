from fastapi import APIRouter, Depends, HTTPException, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controllers.usuario_controller import get_db
from typing import Optional
from controllers import usuario_controller

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_class=HTMLResponse, name="listar_usuarios")
async def listar_usuarios(request: Request, db = Depends(get_db)):
    return usuario_controller.get_all_users_controllers(request,db)
    
    
@router.get("/cadastrar", response_class=HTMLResponse, name="form_cadastrar_usuario")
async def form_cadastrar_usuario(request: Request):
    return usuario_controller.form_cadastrar_usuario(request)


@router.post("/cadastrar", response_class=HTMLResponse, name="cadastrar_usuario")
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(..., min_length=3, max_length=50),
    email: str = Form(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    senha: str = Form(..., min_length=6),
    db = Depends(get_db)
):
    return await usuario_controller.cadastrar_usuario(request, nome , email,senha, db)


@router.get("/{id}", response_class=HTMLResponse, name="obter_usuario")
async def obter_usuario(
    request: Request,
    id: int,
    db = Depends(get_db)
):
    return await usuario_controller.obter_usuario(request,id,db)

@router.get("/{id}/editar", response_class=HTMLResponse, name="form_editar_usuario")
async def form_editar_usuario(
    request: Request,
    id: int,
    db = Depends(get_db)
):
    return await usuario_controller.form_editar_usuario(request, id, db)

@router.post("/{id}/editar", response_class=HTMLResponse, name="processar_edicao_usuario")
async def processar_edicao_usuario(
    request: Request,
    id: int,
    nome: str = Form(..., min_length=3, max_length=50),
    email: str = Form(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    senha: Optional[str] = Form(None, min_length=6),
    db = Depends(get_db)
):
    return await usuario_controller.processar_edicao_usuario(request,id,nome,email,senha, db)

@router.post("/{id}/deletar", name="deletar_usuario")
async def deletar_usuario(
    request: Request,
    id: int,
    db = Depends(get_db)
):
    return await usuario_controller.deletar_usuario(request, id, db)