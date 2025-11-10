from .database import SessionLocal
from . import models
from typing import List

def listar_imoveis(db, limit=100):
    return db.query(models.Imovel).all()

def buscar_imovel(db, imovel_id: int):
    return db.query(models.Imovel).filter(models.Imovel.id_imovel == imovel_id).first()
