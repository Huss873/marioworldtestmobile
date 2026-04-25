from fastapi import FastAPI, Request
import logging
import json

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.post("/api/log")
async def log_data(request: Request):
    try:
        data = await request.json()
        logging.info(f"Dados recebidos: {json.dumps(data)}")
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        return {"error": "Erro interno"}, 500

@app.get("/")
async def root():
    return {"message": "Servidor rodando"}
