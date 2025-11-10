from datetime import date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, ForeignKey, Table, create_engine
)
from sqlalchemy.orm import relationship, declarative_base
from database import Base

# Associação N:N pessoa <-> endereco
pessoa_endereco = Table(
    "pessoa_endereco",
    Base.metadata,
    Column("pessoa_id", Integer, ForeignKey("pessoa.id"), primary_key=True),
    Column("endereco_id", Integer, ForeignKey("endereco.id"), primary_key=True),
    Column("tipo_relacao", String(50))
)

class Endereco(Base):
    __tablename__ = "endereco"
    id = Column(Integer, primary_key=True)
    logradouro = Column(String(200))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(50))
    cep = Column(String(20))
    pessoas = relationship("Pessoa", secondary=pessoa_endereco, back_populates="enderecos")

# Pessoa abstrata
class Pessoa(Base):
    __tablename__ = "pessoa"
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    cpf_cnpj = Column(String(50), unique=True)
    telefone = Column(String(50))
    email = Column(String(200))
    tipo_pessoa = Column(String(50))
    __mapper_args__ = {"polymorphic_on": tipo_pessoa, "polymorphic_identity": "pessoa"}

    enderecos = relationship("Endereco", secondary=pessoa_endereco, back_populates="pessoas")

class Proprietario(Pessoa):
    __tablename__ = "proprietario"
    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    conta_bancaria = Column(String(100))
    imoveis = relationship("Imovel", back_populates="proprietario")
    __mapper_args__ = {"polymorphic_identity": "proprietario"}

class Corretor(Pessoa):
    __tablename__ = "corretor"
    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    salario = Column(Float)
    creci = Column(String(50))
    __mapper_args__ = {"polymorphic_identity": "corretor"}

class Comprador(Pessoa):
    __tablename__ = "comprador"
    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "comprador"}


class Imovel(Base):
    __tablename__ = "imovel"
    id = Column(Integer, primary_key=True)
    id_endereco = Column(Integer, ForeignKey("endereco.id"))
    status_venda = Column(String(50))
    area_total = Column(Float)
    matricula = Column(String(100), unique=True)
    descricao = Column(String(500))
    tipo_imovel = Column(String(50))
    valor_condominio = Column(Float)
    numero_banheiros = Column(Integer)
    numero_quartos = Column(Integer)
    vagas_garagem = Column(Integer)
    proprietario_id = Column(Integer, ForeignKey("proprietario.id"))
    __mapper_args__ = {"polymorphic_on": tipo_imovel, "polymorphic_identity": "imovel"}

    endereco = relationship("Endereco")
    proprietario = relationship("Proprietario", back_populates="imoveis")
    contratos = relationship("Contrato", back_populates="imovel")

class Apartamento(Imovel):
    __tablename__ = "apartamento"
    id = Column(Integer, ForeignKey("imovel.id"), primary_key=True)
    num_suites = Column(Integer)
    area_construida = Column(Float)
    __mapper_args__ = {"polymorphic_identity": "apartamento"}

class Casa(Imovel):
    __tablename__ = "casa"
    id = Column(Integer, ForeignKey("imovel.id"), primary_key=True)
    area_lazer = Column(Boolean, default=False)
    dimensao_lados = Column(Float)
    dimensao_frente = Column(Float)
    __mapper_args__ = {"polymorphic_identity": "casa"}

class Terreno(Imovel):
    __tablename__ = "terreno"
    id = Column(Integer, ForeignKey("imovel.id"), primary_key=True)
    zoneamento = Column(String(50))
    zona_rural = Column(Boolean, default=False)
    cercado = Column(Boolean, default=False)
    __mapper_args__ = {"polymorphic_identity": "terreno"}


class Contrato(Base):
    __tablename__ = "contrato"
    id = Column(Integer, primary_key=True)
    id_imovel = Column(Integer, ForeignKey("imovel.id"))
    data_assinatura = Column(Date, default=date.today)
    valor_total = Column(Float)
    status = Column(String(50))
    tipo = Column(String(50))
    __mapper_args__ = {"polymorphic_on": tipo, "polymorphic_identity": "contrato"}

    imovel = relationship("Imovel", back_populates="contratos")
    pagamentos = relationship("Pagamento", back_populates="contrato")

class Locacao(Contrato):
    __tablename__ = "locacao"
    id = Column(Integer, ForeignKey("contrato.id"), primary_key=True)
    dia_vencimento = Column(Integer)
    valor_aluguel = Column(Float)
    __mapper_args__ = {"polymorphic_identity": "locacao"}

class Venda(Contrato):
    __tablename__ = "venda"
    id = Column(Integer, ForeignKey("contrato.id"), primary_key=True)
    comissao_corretor = Column(Float)
    valor_entrada = Column(Float)
    __mapper_args__ = {"polymorphic_identity": "venda"}

class Pagamento(Base):
    __tablename__ = "pagamento"
    id = Column(Integer, primary_key=True)
    id_contrato = Column(Integer, ForeignKey("contrato.id"))
    valor_pago = Column(Float)
    metodo_pagamento = Column(String(50))
    __mapper_args__ = {"polymorphic_on": metodo_pagamento, "polymorphic_identity": "pagamento"}

    contrato = relationship("Contrato", back_populates="pagamentos")

class Pix(Pagamento):
    __tablename__ = "pix"
    id = Column(Integer, ForeignKey("pagamento.id"), primary_key=True)
    txid = Column(String(200))
    id_pix = Column(String(200))
    __mapper_args__ = {"polymorphic_identity": "pix"}

class Boleto(Pagamento):
    __tablename__ = "boleto"
    id = Column(Integer, ForeignKey("pagamento.id"), primary_key=True)
    codigo_barras = Column(String(200))
    id_boleto = Column(String(200))
    __mapper_args__ = {"polymorphic_identity": "boleto"}
