# benchmark.py
import os
import time
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from models import Base, Endereco, Proprietario, Apartamento, Venda, Imovel, Contrato
from database import Base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/imobiliaria"
)

def run(n=100):
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    start = time.time()
    itens = []
    for i in range(n):
        e = Endereco(logradouro=f"Rua Teste {i}", numero=str(100+i), bairro="Bairro", cidade="Belém", estado="PA", cep=f"66000-{i:03d}")
        p = Proprietario(nome=f"Prop {i}", cpf_cnpj=f"CPF{i:011d}", telefone="(91)99999-0001", email=f"p{i}@ex.com", conta_bancaria="123")
        ap = Apartamento(area_total=50+i, matricula=f"MAT-{1000+i}", descricao="Teste", status_venda="disponivel",
                        num_suites=1, area_construida=50+i, numero_banheiros=1, numero_quartos=1, vagas_garagem=0,
                        proprietario=p, endereco=e, valor_condominio=100.0+i)
        venda = Venda(imovel=ap, valor_total=100000.0 + i, status="negociacao", comissao_corretor=0.05, valor_entrada=1000.0)
        itens.append(ap)
        session.add_all([e,p,ap,venda])
        if i % 50 == 0 and i > 0:
            session.commit()  # commit em batch
    session.commit()
    insert_time = time.time() - start
    print(f"Inserted {n} items in {insert_time:.2f}s (avg {insert_time/n:.4f}s each)")

    # Query time - aggregate
    qstart = time.time()
    media_vendas = (
        session.query(func.avg(Contrato.valor_total)).scalar()
    )
    qtime = time.time() - qstart
    print(f"Aggregate query (avg valor_total) took {qtime:.4f}s, result={media_vendas}")

    session.close()

if __name__ == "__main__":
    run(200)  # padrão: 200 inserções (ajuste conforme necessário)
