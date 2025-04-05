from models.database import get_db
import mysql.connector
from fastapi import Request
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def registrar_log(
    tipo_operacao: str,
    tabela_afetada: str,
    id_registro: Optional[int] = None,
    dados_anteriores: Optional[dict] = None,
    dados_novos: Optional[dict] = None,
    id_usuario: Optional[int] = None,
    request: Optional[Request] = None,
    db: mysql.connector.MySQLConnection = None
):
    try:
        if db is None:
            db = next(get_db())
        
        ip_origem = request.client.host if request else None
        
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO logs (
                tipo_operacao,
                tabela_afetada,
                id_registro,
                dados_anteriores,
                dados_novos,
                id_usuario,
                ip_origem
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                tipo_operacao,
                tabela_afetada,
                id_registro,
                str(dados_anteriores) if dados_anteriores else None,
                str(dados_novos) if dados_novos else None,
                id_usuario,
                ip_origem
            )
        )
        db.commit()
        cursor.close()
    except Exception as e:
        logger.error(f"Falha ao registrar log: {str(e)}")
        # Não falha a operação principal se o log falhar

def obter_logs(db: mysql.connector.MySQLConnection = None):
    try:
        if db is None:
            db = next(get_db())
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logs ORDER BY data_operacao DESC")
        logs = cursor.fetchall()
        cursor.close()
        return logs
    except Exception as e:
        logger.error(f"Erro ao obter logs: {str(e)}")
        return []