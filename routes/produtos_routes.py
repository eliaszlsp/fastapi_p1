from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from models.database import get_db

from controllers import produto_controller


router = APIRouter( tags=["Produtos"]  
)


@router.get("/", response_class=HTMLResponse)
def listar_produtos(request: Request, db=Depends(get_db)):
    return produto_controller.listar_produtos(request, db)


@router.get("/cadastrar", response_class=HTMLResponse)
def form_cadastrar_produto(request: Request):
    return produto_controller.form_cadastrar_produto(request)


@router.post("/cadastrar")
def cadastrar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    preco: float = Form(...),
    estoque: int = Form(...),
    db=Depends(get_db),
):
    return produto_controller.cadastrar_produto(request, nome, descricao, preco, estoque, db)


@router.get("/{id}", response_class=HTMLResponse)
def obter_produto(request: Request, id: int, db=Depends(get_db)):
    return produto_controller.obter_produto(request, id, db)


@router.get("/{id}/editar", response_class=HTMLResponse)
def form_editar_produto(request: Request, id: int, db=Depends(get_db)):
    return produto_controller.form_editar_produto(request, id, db)


@router.put("/{id}/editar")
def editar_produto(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    preco: float = Form(...),
    estoque: int = Form(...),
    db=Depends(get_db),
):
    return produto_controller.editar_produto(request, id, nome, descricao, preco, estoque, db)


@router.delete("/{id}/deletar")
def deletar_produto(request: Request, id: int, db=Depends(get_db)):
    return produto_controller.deletar_produto(request, id, db)