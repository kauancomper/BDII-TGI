from sqlalchemy import func
from database import SessionLocal
from models import Corretor, Venda

def media_vendas_por_corretor():
    """
    Retorna lista de tuplas (nome_corretor, media_vendas)
    """
    session = SessionLocal()
    try:
        resultado = (
            session.query(
                Corretor.nome,
                func.avg(Venda.valor).label('media_vendas')
            )
            .join(Venda, Corretor.vendas)
            .group_by(Corretor.nome)
            .all()
        )
        return resultado
    finally:
        session.close()