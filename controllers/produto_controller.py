from fastapi import Depends, HTTPException, Form, Request
from fastapi.responses import  RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import starlette.status as status
from models.produto_model import (
    ProdutoCreate,
    get_all_produtos,
    get_produto_by_id,
    create_produto,
    update_produto,
    delete_produto
)
from models.database import get_db

templates = Jinja2Templates(directory="templates")


class ProdutoSchema(BaseModel):
    nome: str
    descricao: Optional[str] = ""
    preco: float
    estoque: int


def listar_produtos(request: Request, db=Depends(get_db)):
    try:
        produtos = get_all_produtos(db)
        return templates.TemplateResponse("produtos/lista.html", {
            "request": request,
            "produtos": produtos
        })
    except Exception as e:
        print(f"Erro ao acessar banco: {e}")
        return templates.TemplateResponse("produtos/lista.html", {
            "request": request,
            "produtos": [],
            "messages": [{
                "message": "Erro ao carregar produtos do banco de dados.",
                "category": "danger"
            }]
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def form_cadastrar_produto(request: Request):
    return templates.TemplateResponse("produtos/cadastro.html", {
        "request": request
    })


def cadastrar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    preco: float = Form(...),
    estoque: int = Form(...),
    db=Depends(get_db)
):
    try:
        produto_data = ProdutoCreate(
            nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        produto_id = create_produto(produto_data, db)

        if produto_id:
            return RedirectResponse(url="/produtos", status_code=303)

        raise ValueError("Erro ao cadastrar produto.")

    except ValueError as e:
        return templates.TemplateResponse("produtos/cadastro.html", {
            "request": request,
            "errors": [str(e)],
            "form_data": {
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "estoque": estoque
            }
        }, status_code=status.HTTP_400_BAD_REQUEST)


def obter_produto(request: Request, id: int, db=Depends(get_db)):
    try:
        produto = get_produto_by_id(id, db)
        if produto:
            return templates.TemplateResponse("produtos/detalhes.html", {
                "request": request,
                "produto": produto
            })
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    except Exception as e:
        print(f"Erro ao obter produto: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao encontrar o produto")


def form_editar_produto(request: Request, id: int, db=Depends(get_db)):
    try:
        produto = get_produto_by_id(id, db)
        if not produto:
            raise HTTPException(
                status_code=404, detail="Produto não encontrado")
        return templates.TemplateResponse("produtos/editar.html", {
            "request": request,
            "produto": produto
        })
    except Exception as e:
        print(f"Erro ao carregar formulário de edição: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Formulario não encontrado")


def editar_produto(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...),
    db=Depends(get_db)
):
    try:
        produto_atual = get_produto_by_id(id, db)
        if not produto_atual:
            raise HTTPException(
                status_code=404, detail="Produto não encontrado")

        produto_data = ProdutoCreate(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque
        )
        update_produto(id, produto_data, db)
        return RedirectResponse(url="/produtos", status_code=303)

    except ValueError as e:
        return templates.TemplateResponse("produtos/editar.html", {
            "request": request,
            "produto": {
                "id": id,
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "estoque": estoque
            },
            "errors": [str(e)]
        }, status_code=status.HTTP_400_BAD_REQUEST)


def deletar_produto(request: Request, id: int, db=Depends(get_db)):
    try:
        produto = get_produto_by_id(id, db)
        if produto is None:
            raise HTTPException(
                status_code=404, detail="Produto não encontrado")

        affected_rows = delete_produto(id, db)
        if affected_rows > 0:
            return RedirectResponse(url="/produtos", status_code=303)

        raise HTTPException(status_code=400, detail="Falha ao deletar produto")

    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao deletar o Produto"
        )
