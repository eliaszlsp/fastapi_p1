from fastapi import Depends
import mysql.connector
from config import Config
import logging

logger = logging.getLogger(__name__)

def get_db():
    config = Config()
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD
    )
    
    try:
        # Verifica e cria o banco de dados se não existir
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB}")
        cursor.execute(f"USE {config.MYSQL_DB}")
        
        # Criação das tabelas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tipo_operacao VARCHAR(20) NOT NULL,
            tabela_afetada VARCHAR(50) NOT NULL,
            id_registro INT,
            dados_anteriores TEXT,
            dados_novos TEXT,
            id_usuario INT,
            data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_origem VARCHAR(45)
        )
        """)
        
        conn.commit()
        cursor.close()
        
        # Reconecta usando o banco de dados específico
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        yield conn
    except Exception as e:
        logger.error(f"Erro ao configurar banco de dados: {str(e)}")
        raise
    finally:
        if conn.is_connected():
            conn.close()