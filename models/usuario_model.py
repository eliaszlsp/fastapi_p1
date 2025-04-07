from pydantic import BaseModel
from models.database import get_db
import mysql.connector
from passlib.context import CryptContext

class UsuarioBase(BaseModel):
    nome: str
    email: str
    senha: str
class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

def create_usuario(usuario: UsuarioCreate, db: mysql.connector.MySQLConnection):
    try:
        #usuario.hash_password()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, usuario.senha),
        )
        db.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: 
            err.msg = "Este e-mail já está cadastrado"
        raise ValueError(f"Erro ao criar usuário: {err.msg}")

def get_usuario_by_id(id: int, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = %s", (id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        raise ValueError(f"Erro ao buscar usuário: {err.msg}")

def get_all_usuarios(db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email FROM usuarios ORDER BY nome")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise ValueError(f"Erro ao listar usuários: {err.msg}")

def update_usuario(id: int, update_data: dict, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        
        if 'senha' in update_data:
            update_data['senha'] = update_data['senha']
        
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(id)
        
        cursor.execute(
            f"UPDATE usuarios SET {set_clause} WHERE id = %s",
            values
        )
        db.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        db.rollback()
        raise ValueError(f"Erro ao atualizar usuário: {err.msg}")

def delete_usuario(id: int, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        db.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        db.rollback()
        raise ValueError(f"Erro ao deletar usuário: {err.msg}")