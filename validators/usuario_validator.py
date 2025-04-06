from pydantic import BaseModel, EmailStr, Field, ValidationError


class UsuarioSchema(BaseModel):
    nome: str = Field(..., min_length=3,
                      description="O nome deve ter pelo menos 3 caracteres")
    email: EmailStr = Field(..., description="Email inválido")
    senha: str = Field(..., min_length=6,
                       description="A senha deve ter pelo menos 6 caracteres")


class UsuarioValidator:
    @staticmethod
    def validate(data: dict):
        try:
            UsuarioSchema(**data)
            return {"valid": True}
        except ValidationError as e:
            return {"valid": False, "errors": e.errors()}
