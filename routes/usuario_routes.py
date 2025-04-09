from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from controllers.usuario_controller import get_db
from typing import Optional
from controllers import usuario_controller

router = APIRouter(tags=["Usuários"])


@router.get("/", response_class=HTMLResponse, )
async def listar_usuarios(request: Request, db=Depends(get_db)):
    return usuario_controller.get_all_users_controllers(request, db)


@router.get("/cadastrar", response_class=HTMLResponse, )
async def form_cadastrar_usuario(request: Request):
    return usuario_controller.form_cadastrar_usuario(request)


@router.post("/cadastrar", response_class=HTMLResponse, )
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(..., min_length=3, max_length=50),
    email: str = Form(...,
                      regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    senha: str = Form(..., min_length=6),
    db=Depends(get_db)
):
    return await usuario_controller.cadastrar_usuario(request, nome, email, senha, db)


@router.get("/{id}", response_class=HTMLResponse, name="obter_usuario")
async def obter_usuario(
    request: Request,
    id: int,
    db=Depends(get_db)
):
    return usuario_controller.obter_usuario(request, id, db)


@router.get("/{id}/editar", response_class=HTMLResponse, )
async def form_editar_usuario(
    request: Request,
    id: int,
    db=Depends(get_db)
):
    return usuario_controller.form_editar_usuario(request, id, db)


@router.put("/{id}/editar", response_class=HTMLResponse, )
async def processar_edicao_usuario(
    request: Request,
    id: int,
    nome: str = Form(..., min_length=3, max_length=50),
    email: str = Form(...,
                      regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    senha: Optional[str] = Form(None, min_length=6),
    db=Depends(get_db)
):
    return await usuario_controller.processar_edicao_usuario(request, id, nome, email, senha, db)


@router.delete("/{id}/deletar", name="deletar_usuario")
async def deletar_usuario(
    request: Request,
    id: int,
    db=Depends(get_db)
):
    return usuario_controller.deletar_usuario(request, id, db)