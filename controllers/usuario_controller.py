from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.usuario_model import (
    UsuarioCreate,
    get_all_usuarios,
    get_usuario_by_id,
    create_usuario,
    delete_usuario,
    update_usuario
)
from models.database import get_db
from typing import Optional
import starlette.status as status

templates = Jinja2Templates(directory="templates")


def set_flash(request: Request, message: str, category: str = "success"):
    if not hasattr(request.state, 'session'):
        request.state.session = {}
    request.state.session['flash'] = {'message': message, 'category': category}


def get_flash(request: Request):
    if hasattr(request.state, 'session') and 'flash' in request.state.session:
        flash = request.state.session.pop('flash')
        return flash
    return None


def get_all_users_controllers(request: Request, db=Depends(get_db)):
    try:
        usuarios = get_all_usuarios(db)
        flash = get_flash(request)
        messages = [flash] if flash else []
        return templates.TemplateResponse(
            "usuarios/lista.html",
            {"request": request, "usuarios": usuarios, "messages": messages}
        )
    except Exception as e:
        print(f"Erro ao listar usuários: {str(e)}")
        return templates.TemplateResponse(
            "usuarios/lista.html",
            {"request": request, "usuarios": [], "messages": [
                {"message": "Erro ao carregar usuários", "category": "danger"}]
             },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def form_cadastrar_usuario(request: Request):
    return templates.TemplateResponse(
        "usuarios/cadastro.html",
        {"request": request, "errors": [], "form_data": {}}
    )


async def cadastrar_usuario(request: Request, nome, email, senha, db=Depends(get_db)):
    try:
        usuario_data = UsuarioCreate(nome=nome, email=email, senha=senha)
        usuario_id = create_usuario(usuario_data, db)

        if not usuario_id:
            raise ValueError("Não foi possível criar o usuário")

        set_flash(request, "Usuário cadastrado com sucesso!")
        return RedirectResponse(
            url=request.url_for("listar_usuarios"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "usuarios/cadastro.html",
            {
                "request": request,
                "errors": [str(e)],
                "form_data": {"nome": nome, "email": email}
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )


def obter_usuario(request: Request, id=int, db=Depends(get_db)):
    try:
        usuario = get_usuario_by_id(id, db)
        if not usuario:
            raise HTTPException(
                status_code=404, detail="Usuário não encontrado")

        return templates.TemplateResponse(
            "usuarios/detalhes.html",
            {"request": request, "usuario": usuario}
        )
    except Exception as e:
        print(f"Erro ao obter usuário {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao carregar usuário"
        )


def form_editar_usuario(request: Request, id: int, db=Depends(get_db)):
    try:
        usuario = get_usuario_by_id(id, db)
        if not usuario:
            raise HTTPException(
                status_code=404, detail="Usuário não encontrado")

        return templates.TemplateResponse(
            "usuarios/editar.html",
            {"request": request, "usuario": usuario, "errors": []}
        )
    except Exception as e:
        print(
            f"Erro ao carregar formulário de edição para usuário {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao carregar formulário de edição"
        )


async def processar_edicao_usuario(request: Request, id: int, nome: str, email: str, senha: Optional[str], db=Depends(get_db)):
    try:

        usuario_atual = get_usuario_by_id(id, db)
        if not usuario_atual:
            raise HTTPException(
                status_code=404, detail="Usuário não encontrado")

        update_data = {"nome": nome, "email": email}
        if senha and senha.strip():
            update_data["senha"] = senha

        rows_updated = update_usuario(id, update_data, db)
        if rows_updated == 0:
            raise ValueError("Nenhum usuário foi atualizado")

        set_flash(request, "Usuário atualizado com sucesso!")
        return RedirectResponse(
            url=request.url_for("obter_usuario", id=id),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except ValueError as e:
        print(f"Erro ao editar usuário {id}: {str(e)}")
        usuario = get_usuario_by_id(id, db)
        return templates.TemplateResponse(
            "usuarios/editar.html",
            {
                "request": request,
                "usuario": usuario,
                "errors": [str(e)]
            },
            status_code=status.HTTP_404_NOT_FOUND
        )


def deletar_usuario(request: Request, id: int, db=Depends(get_db)):
    try:

        affected_rows = delete_usuario(id, db)
        if affected_rows == 0:
            raise HTTPException(
                status_code=404, detail="Usuário não encontrado")

        set_flash(request, "Usuário excluído com sucesso!")
        return RedirectResponse(
            url=request.url_for("listar_usuarios"),
            status_code=status.HTTP_303_SEE_OTHER
        )

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        print(f"Erro ao deletar usuário {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar o usuario"
        )
