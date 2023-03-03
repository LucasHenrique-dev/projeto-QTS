from fastapi import FastAPI
from pydantic import BaseModel

class Dados(BaseModel):
    name: str
    price: float
    is_offer: bool = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/gerador_qts/")
async def gera_qts(dado: Dados):
    print(dado)
    return dado
