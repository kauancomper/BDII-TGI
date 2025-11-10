from sqlalchemy.orm import Session
from . import models
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError

def popular_dados(db: Session):
        # evita duplicar inserção
        if db.query(models.Pessoa).first():
            return

        # tipos
        tipos_pessoa = [models.TipoPessoa(descricao="proprietario"),
                        models.TipoPessoa(descricao="corretor"),
                        models.TipoPessoa(descricao="cliente")]
        db.add_all(tipos_pessoa)
        db.commit()

        tipos_end = [models.TipoEndereco(descricao="residencial"),
                    models.TipoEndereco(descricao="comercial"),
                    models.TipoEndereco(descricao="cobertura")]
        db.add_all(tipos_end); db.commit()

        tipo_imovel = [models.TipoImovel(descricao="Apartamento"),
                    models.TipoImovel(descricao="Casa"),
                    models.TipoImovel(descricao="Cobertura")]
        db.add_all(tipo_imovel); db.commit()

        status_imovel = [models.StatusImovel(descricao="disponivel"),
                        models.StatusImovel(descricao="alugado"),
                        models.StatusImovel(descricao="vendido")]
        db.add_all(status_imovel); db.commit()

        # pessoas (proprietários / corretores / clientes)
        p1 = models.Pessoa(nome="João Silva", cpf_cnpj="11122233344", email="joao@example.com", telefone="(91)99999-0001", id_tipo_pessoa=1)
        p2 = models.Pessoa(nome="Maria Souza", cpf_cnpj="22233344455", email="maria@example.com", telefone="(91)99999-0002", id_tipo_pessoa=2)
        p3 = models.Pessoa(nome="Pedro Lima", cpf_cnpj="33344455566", email="pedro@example.com", telefone="(91)99999-0003", id_tipo_pessoa=3)
        db.add_all([p1,p2,p3]); db.commit()

        # endereços
        e1 = models.Endereco(logradouro="Rua das Flores", numero="123", bairro="Centro", cidade="Marabá", estado="PA", cep="68500-000")
        e2 = models.Endereco(logradouro="Av. Amazonas", numero="456", bairro="Jardim", cidade="Belém", estado="PA", cep="66000-000")
        e3 = models.Endereco(logradouro="Rua Pará", numero="789", bairro="Bela Vista", cidade="Altamira", estado="PA", cep="68370-000")
        db.add_all([e1,e2,e3]); db.commit()

        # vincular pessoa <-> endereco (pessoa_endereco)
        db.add_all([
            models.PessoaEndereco(id_pessoa=1, id_endereco=1, id_tipo_endereco=1),
            models.PessoaEndereco(id_pessoa=2, id_endereco=2, id_tipo_endereco=2),
            models.PessoaEndereco(id_pessoa=3, id_endereco=3, id_tipo_endereco=1),
        ])
        db.commit()

        # caracteristicas
        c1 = models.Caracteristica(nome="Piscina", descricao="Piscina adulto")
        c2 = models.Caracteristica(nome="Churrasqueira", descricao="Área com churrasqueira")
        c3 = models.Caracteristica(nome="Garagem", descricao="2 vagas")
        db.add_all([c1,c2,c3]); db.commit()

        # imoveis
        im1 = models.Imovel(titulo="Apartamento Central", descricao="2 quartos, ótima localização", id_tipo_imovel=1, id_status_imovel=1,
                            valor_venda=350000, valor_aluguel=1800, area_m2=75.0, quartos=2, banheiros=1, vagas_garagem=1,
                            data_cadastro=date.today(), id_proprietario=1, id_endereco=1)
        im2 = models.Imovel(titulo="Casa Jardim", descricao="3 quartos, quintal", id_tipo_imovel=2, id_status_imovel=1,
                            valor_venda=520000, valor_aluguel=2500, area_m2=150.0, quartos=3, banheiros=2, vagas_garagem=2,
                            data_cadastro=date.today(), id_proprietario=1, id_endereco=2)
        im3 = models.Imovel(titulo="Cobertura Luxo", descricao="Cobertura com vista", id_tipo_imovel=3, id_status_imovel=1,
                            valor_venda=850000, valor_aluguel=5200, area_m2=200.0, quartos=4, banheiros=3, vagas_garagem=3,
                            data_cadastro=date.today(), id_proprietario=2, id_endereco=3)
        db.add_all([im1,im2,im3]); db.commit()

        # fotos
        f1 = models.Foto(id_imovel=1, url="https://example.com/im1.jpg", descricao="fachada", ordem=1)
        f2 = models.Foto(id_imovel=2, url="https://example.com/im2.jpg", descricao="sala", ordem=1)
        f3 = models.Foto(id_imovel=3, url="https://example.com/im3.jpg", descricao="vista", ordem=1)
        db.add_all([f1,f2,f3]); db.commit()

        # associar caracteristicas
        im1.caracteristicas.append(c1)
        im1.caracteristicas.append(c3)
        im2.caracteristicas.append(c2)
        im3.caracteristicas.append(c1)
        db.commit()

        # contratos (inclui tipo_contrato/status_contrato)
        tc1 = models.TipoContrato(descricao="venda")
        tc2 = models.TipoContrato(descricao="aluguel")
        tc3 = models.TipoContrato(descricao="pre-contrato")
        db.add_all([tc1,tc2,tc3]); db.commit()

        sc1 = models.StatusContrato(descricao="ativo")
        sc2 = models.StatusContrato(descricao="cancelado")
        sc3 = models.StatusContrato(descricao="concluido")
        db.add_all([sc1,sc2,sc3]); db.commit()

        # contratos de exemplo (venda) - 3 contratos
        contr1 = models.Contrato(id_tipo_contrato=1, id_status_contrato=1, id_imovel=1, id_cliente=3, id_corretor=2, id_proprietario=1,
                                data_inicio=date.today(), data_fim=None, valor=350000, comissao_percentual=5.0)
        contr2 = models.Contrato(id_tipo_contrato=1, id_status_contrato=3, id_imovel=2, id_cliente=3, id_corretor=2, id_proprietario=1,
                                data_inicio=date.today(), data_fim=None, valor=520000, comissao_percentual=6.0)
        contr3 = models.Contrato(id_tipo_contrato=2, id_status_contrato=1, id_imovel=3, id_cliente=3, id_corretor=2, id_proprietario=2,
                                data_inicio=date.today(), data_fim=None, valor=850000, comissao_percentual=5.5)
        db.add_all([contr1,contr2,contr3]); db.commit()

        # metodos e status pagamento
        mp1 = models.MetodoPagamento(descricao="Transferência")
        mp2 = models.MetodoPagamento(descricao="Cartão")
        mp3 = models.MetodoPagamento(descricao="Dinheiro")
        db.add_all([mp1,mp2,mp3]); db.commit()

        sp1 = models.StatusPagamento(descricao="pendente")
        sp2 = models.StatusPagamento(descricao="pago")
        sp3 = models.StatusPagamento(descricao="estornado")
        db.add_all([sp1,sp2,sp3]); db.commit()

        # pagamentos
        pag1 = models.Pagamento(id_contrato=1, data_pagamento=date.today(), valor_pago=350000, id_metodo_pagamento=1, id_status_pagamento=2)
        pag2 = models.Pagamento(id_contrato=2, data_pagamento=date.today(), valor_pago=520000, id_metodo_pagamento=2, id_status_pagamento=2)
        pag3 = models.Pagamento(id_contrato=3, data_pagamento=None, valor_pago=0, id_metodo_pagamento=1, id_status_pagamento=1)
        db.add_all([pag1,pag2,pag3]); db.commit()

        # agendamentos e status
        sa1 = models.StatusAgendamento(descricao="agendado")
        sa2 = models.StatusAgendamento(descricao="realizado")
        sa3 = models.StatusAgendamento(descricao="cancelado")
        db.add_all([sa1,sa2,sa3]); db.commit()

        ag1 = models.Agendamento(id_imovel=1, id_cliente=3, id_corretor=2, data_hora=datetime.now(), id_status_agendamento=1, observacoes="Visita rápida")
        ag2 = models.Agendamento(id_imovel=2, id_cliente=3, id_corretor=2, data_hora=datetime.now(), id_status_agendamento=1, observacoes="Segunda visita")
        ag3 = models.Agendamento(id_imovel=3, id_cliente=3, id_corretor=2, data_hora=datetime.now(), id_status_agendamento=1, observacoes="Visita VIP")
        db.add_all([ag1,ag2,ag3]); db.commit()
