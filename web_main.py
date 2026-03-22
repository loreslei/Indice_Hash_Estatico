from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from paginas_hash_web import HashTable, Page, table_scan
from fastapi.middleware.cors import CORSMiddleware
import time


class ConfiguracaoBanco(BaseModel):
    tuples_per_page: int
    bucket_capacity: int

words_list = []
pages = []
hash_table = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global words_list
    with open("words.txt", "r") as f:
        words_list = f.read().splitlines()
    print("Palavras carregadas. Aguardando configuração via POST /inicializar")
    yield
    print("Limpando a memória...")
    words_list.clear()
    pages.clear()

app = FastAPI(title="API de Busca em Banco de Dados", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "https://front-end-hash.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/inicializar")
def inicializar_banco(config: ConfiguracaoBanco):
    global pages, hash_table
    
    if config.tuples_per_page <= 0 or config.bucket_capacity <= 0:
        raise HTTPException(
            status_code=400, 
            detail="As quantidades de tuplas e a capacidade do bucket devem ser maiores que zero."
        )
        
    pages = Page.paginate(words_list, config.tuples_per_page)
    hash_table = HashTable(config.bucket_capacity)
    
    for page in pages:
        for key in page.records:
            hash_table.insert_hash(key, page.number)
            
    return {
        "mensagem": "Banco inicializado com sucesso!",
        "configuracao_aplicada": {
            "tuplas_por_pagina": config.tuples_per_page,
            "capacidade_do_bucket": config.bucket_capacity
        },
        "total_registros_inseridos": sum([len(p.records) for p in pages]),
        "total_paginas_geradas": len(pages)
    }

@app.get("/estatisticas")
def obter_estatisticas():
    if not hash_table:
        raise HTTPException(status_code=400, detail="Inicialize o banco primeiro.")
    stats = hash_table.get_statistics()
    return {
        "total_registros": sum([len(p.records) for p in pages]),
        "total_paginas": len(pages),
        "estatisticas_hash": stats
    }

@app.get("/buscar/{word}")
def buscar_palavra(word: str):
    if not hash_table:
        raise HTTPException(status_code=400, detail="Inicialize o banco primeiro.")

    start_time_index = time.perf_counter()
    resultado_hash = hash_table.search(word)
    end_time_index = time.perf_counter()
    
    start_time_table_scan = time.perf_counter() 
    resultado_scan = table_scan(pages, word)
    end_time_table_scan = time.perf_counter()
    
    # ... código de buscar o resultado_hash e resultado_scan

    time_spent_hash_index = round(end_time_index - start_time_index, 6)
    time_spent_table_scan = round(end_time_table_scan - start_time_table_scan, 6)
    
    # Criamos tempos seguros (no mínimo 1 microssegundo) para evitar divisão por zero
    safe_hash_time = max(time_spent_hash_index, 0.000001)
    safe_scan_time = max(time_spent_table_scan, 0.000001)
    
    # Cálculo real, mesmo se o hash tiver sido rápido demais para o Python medir
    speed_gain = 100 - ((safe_hash_time / safe_scan_time) * 100)
    speedup = (safe_scan_time - safe_hash_time) / safe_hash_time
        
    return {
        "palavra_buscada": word,
        "resultados": {
            "indice_hash": resultado_hash,
            "table_scan": resultado_scan
        },
        "comparacao_tempo": {
            "tempo_hash_segundos": time_spent_hash_index, # Exibe o tempo real na tela
            "tempo_scan_segundos": time_spent_table_scan,
            "reducao_tempo_pct": round(speed_gain, 2),
            "ganho_velocidade_x": round(speedup, 2)
        }
    }

@app.get("/estrutura")
def obter_estrutura(detalhado: bool = False):
    if not hash_table:
        raise HTTPException(status_code=400, detail="Inicialize o banco primeiro.")
    estrutura_dados = hash_table.get_hash_structure(incluir_registros=detalhado)
    return {
        "total_indices_unicos": len(estrutura_dados),
        "estrutura_indice": estrutura_dados
    }