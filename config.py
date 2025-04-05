import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_32_caracteres')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'carlos25')
    MYSQL_DB = os.getenv('MYSQL_DB', 'carlos')
