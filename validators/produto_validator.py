from pydantic import BaseModel, Field, ValidationError
from typing import Optional


class ProdutoSchema(BaseModel):
    nome: str = Field(..., min_length=3,
                      description="O nome do produto deve ter pelo menos 3 caracteres")
    descricao: Optional[str] = Field(
        "", description="A descrição do produto é opcional")
    preco: float = Field(..., gt=1,
                         description="O preço deve ser um valor positivo")
    estoque: int = Field(..., ge=1,
                         description="O estoque deve ser um número inteiro maior ou igual a 1")


class ProdutoValidator:
    @staticmethod
    def validate(data: dict):
        try:
            ProdutoSchema(**data)
            return {"valid": True}
        except ValidationError as e:
            return {"valid": False, "errors": e.errors()}
