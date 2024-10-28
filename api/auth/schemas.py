import re
from pydantic import BaseModel, field_validator


class User(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z0-9@]+$', value):  # Permite letras maiúsculas e minúsculas, números e o símbolo @
            raise ValueError('Formato de nome de usuário inválido')
        return value
