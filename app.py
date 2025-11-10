from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import Base, engine, SessionLocal
from . import insert_data, queries, crud
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Imobiliária - FastAPI")

# mount static (empty or add css)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# create schema
Base.metadata.create_all(bind=engine)

# startup: popular dados
@app.on_event("startup")
def startup():
    db = SessionLocal()
    insert_data.popular_dados(db)
    db.close()
    logger.info("Startup: dados populados (se necessário).")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db=Depends(get_db)):
    imoveis = crud.listar_imoveis(db)
    return templates.TemplateResponse("index.html", {"request": request, "imoveis": imoveis})

@app.get("/imoveis", response_class=HTMLResponse)
def view_imoveis(request: Request, db=Depends(get_db)):
    imoveis = crud.listar_imoveis(db)
    return templates.TemplateResponse("imoveis.html", {"request": request, "imoveis": imoveis})

@app.get("/consultas", response_class=HTMLResponse)
def consultas(request: Request, db=Depends(get_db)):
    media_por_corretor = queries.media_vendas_por_corretor(db)
    por_cidade = queries.imoveis_por_cidade_disponiveis(db)
    return templates.TemplateResponse("consultas.html", {
        "request": request,
        "media_por_corretor": media_por_corretor,
        "por_cidade": por_cidade
    })

# API endpoints (json) para consumo
@app.get("/api/consultas/media_vendas")
def api_media_vendas(db=Depends(get_db)):
    return queries.media_vendas_por_corretor(db)

@app.get("/api/consultas/imoveis_por_cidade")
def api_imoveis_cidade(db=Depends(get_db)):
    return queries.imoveis_por_cidade_disponiveis(db)
