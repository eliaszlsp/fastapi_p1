from pydantic import BaseModel, Field
from typing import Optional
from models.database import get_db
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
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    return cursor.fetchone()


def get_all_produtos(db: mysql.connector.MySQLConnection):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    return cursor.fetchall()


def create_produto(produto: ProdutoCreate, db: mysql.connector.MySQLConnection):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)",
        (produto.nome, produto.descricao, produto.preco, produto.estoque),
    )
    db.commit()
    return cursor.lastrowid


def update_produto(id: int, produto: ProdutoBase, db: mysql.connector.MySQLConnection):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome=%s, descricao=%s, preco=%s, estoque=%s WHERE id=%s",
        (produto.nome, produto.descricao, produto.preco, produto.estoque, id),
    )
    db.commit()
    return cursor.rowcount


def delete_produto(id: int, db: mysql.connector.MySQLConnection):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
    db.commit()
    return cursor.rowcount
