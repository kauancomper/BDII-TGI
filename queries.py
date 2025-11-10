from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def media_vendas_por_corretor(db: Session):
    """
    Média do valor dos contratos do tipo 'venda' por corretor.
    """
    sub = (
        db.query(
            models.Contrato.id_corretor.label("corretor_id"),
            func.avg(models.Contrato.valor).label("media_venda")
        )
        .join(models.TipoContrato, models.Contrato.id_tipo_contrato == models.TipoContrato.id_tipo_contrato)
        .filter(models.TipoContrato.descricao == "venda")
        .group_by(models.Contrato.id_corretor)
        .subquery()
    )

    resultados = (
        db.query(models.Pessoa.nome, sub.c.media_venda)
        .join(sub, sub.c.corretor_id == models.Pessoa.id_pessoa)
        .all()
    )

    return [{"corretor": r[0], "media_venda": float(r[1]) if r[1] is not None else None} for r in resultados]

def imoveis_por_cidade_disponiveis(db: Session):
    """
    Count de imóveis com status 'disponivel' por cidade.
    """
    resultados = (
        db.query(models.Endereco.cidade, func.count(models.Imovel.id_imovel))
        .join(models.Imovel, models.Imovel.id_endereco == models.Endereco.id_endereco)
        .join(models.StatusImovel, models.Imovel.id_status_imovel == models.StatusImovel.id_status_imovel)
        .filter(models.StatusImovel.descricao == "disponivel")
        .group_by(models.Endereco.cidade)
        .all()
    )
    return [{"cidade": r[0], "qtd_disponiveis": int(r[1])} for r in resultados]
