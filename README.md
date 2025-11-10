# BDII-TGI
# Projeto BDII-TGI — Sistema Imobiliária (FastAPI + SQLAlchemy + Postgres)

## Descrição
Aplicação demonstrando mapeamento objeto-relacional (ORM) com SQLAlchemy, backend, FastAPI, banco PostgreSQL.

Mantém a modelagem (DER): tabelas `pessoa`, `endereco`, `imovel`, `contrato`, `pagamento`, `agendamento`, e tabelas auxiliares (tipos/status/características).

## Como rodar (Docker)
1. Ter Docker & Docker Compose instalado.
2. Na pasta do projeto:
```bash
docker compose up --build
