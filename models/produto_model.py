from pydantic import BaseModel, Field
from typing import Optional
import mysql.connector


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=3)
    descricao: Optional[str] = None
    preco: float = Field(..., gt=0)
    estoque: int = Field(..., ge=0)


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True


def get_produto_by_id(id: int, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Erro ao buscar produto por ID: {err}")
        return False


def get_all_produtos(db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao buscar todos os produtos: {err}")
        return []


def create_produto(produto: ProdutoCreate, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)",
            (produto.nome, produto.descricao, produto.preco, produto.estoque),
        )
        db.commit()
        print("aqui", cursor.lastrowid)
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Erro ao criar produto: {err}")
        return False


def update_produto(id: int, produto: ProdutoBase, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE produtos SET nome=%s, descricao=%s, preco=%s, estoque=%s WHERE id=%s",
            (produto.nome, produto.descricao, produto.preco, produto.estoque, id),
        )
        db.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar produto: {err}")
        return 0


def delete_produto(id: int, db: mysql.connector.MySQLConnection):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
        db.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao deletar produto: {err}")
        return 0
