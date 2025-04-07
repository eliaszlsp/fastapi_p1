from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from models.produto_model import ProdutoCreate, get_all_produtos, get_produto_by_id, create_produto, update_produto, delete_produto
from models.database import get_db
from models.log_model import registrar_log
import mysql.connector

templates = Jinja2Templates(directory="templates")

class ProdutoSchema(BaseModel):
    nome: str
    descricao: Optional[str] = ""
    preco: float
    estoque: int

def listar_produtos(request: Request, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produtos = get_all_produtos(db)
    return templates.TemplateResponse("produtos/lista.html", {"request": request, "produtos": produtos})

def form_cadastrar_produto(request: Request):
    return templates.TemplateResponse("produtos/cadastro.html", {"request": request})

def cadastrar_produto(request: Request, nome, descricao, preco, estoque, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produto_data = ProdutoCreate(
        nome=nome, descricao=descricao, preco=preco, estoque=estoque)
    produto_id = create_produto(produto_data, db)

    if produto_id:
        registrar_log(
            tipo_operacao="CREATE",
            tabela_afetada="produtos",
            id_registro=produto_id,
            dados_novos=produto_data.dict(),
            request=request,
            db=db
        )
        return RedirectResponse(url="/produtos", status_code=303)

    return templates.TemplateResponse("produtos/cadastro.html", {
        "request": request,
        "errors": ["Erro ao cadastrar produto"]
    })

def obter_produto(request: Request, id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produto = get_produto_by_id(id, db)
    if produto:
        return templates.TemplateResponse("produtos/detalhes.html", {"request": request, "produto": produto})
    raise HTTPException(status_code=404, detail="Produto não encontrado")

def form_editar_produto(request: Request, id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produto = get_produto_by_id(id, db)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse("produtos/editar.html", {"request": request, "produto": produto})

def editar_produto(request: Request, id: int, nome: str, descricao: str, preco: float, estoque: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produto_atual = get_produto_by_id(id, db)

    produto_data = ProdutoCreate(
        nome=nome, descricao=descricao, preco=preco, estoque=estoque)
    affected_rows = update_produto(id, produto_data, db)

    if affected_rows > 0:
        registrar_log(
            tipo_operacao="UPDATE",
            tabela_afetada="produtos",
            id_registro=id,
            dados_anteriores={
                "nome": produto_atual["nome"],
                "descricao": produto_atual["descricao"],
                "preco": float(produto_atual["preco"]),
                "estoque": produto_atual["estoque"]
            },
            dados_novos=produto_data.dict(),
            request=request,
            db=db
        )

        return RedirectResponse(url="/produtos", status_code=303)
    elif affected_rows == 0:
        return RedirectResponse(url="/produtos", status_code=303)

    raise HTTPException(
        status_code=400, detail="Nenhum produto foi atualizado")

def deletar_produto(request: Request, id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    produto = get_produto_by_id(id, db)

    affected_rows = delete_produto(id, db)
    if affected_rows > 0:
        registrar_log(
            tipo_operacao="DELETE",
            tabela_afetada="produtos",
            id_registro=id,
            dados_anteriores={
                "nome": produto["nome"],
                "descricao": produto["descricao"],
                "preco": float(produto["preco"]),
                "estoque": produto["estoque"]
            },
            request=request,
            db=db
        )
        return RedirectResponse(url="/produtos", status_code=303)
    raise HTTPException(status_code=404, detail="Produto não encontrado")
