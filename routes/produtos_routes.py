from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from models.produto_model import ProdutoCreate, get_all_produtos, get_produto_by_id, create_produto, update_produto, delete_produto
from models.database import get_db
from models.log_model import registrar_log
from controllers import produto_controller
import mysql.connector

router = APIRouter()


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


@router.post("/{id}/editar")
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


@router.post("/{id}/deletar")
def deletar_produto(request: Request, id: int, db=Depends(get_db)):
    return produto_controller.deletar_produto(request, id, db)
