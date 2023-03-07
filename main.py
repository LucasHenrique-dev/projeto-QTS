from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

def retorna_valor_campo(col,campus):
    
    return campus.idCampus if col == 1 else campus.desc

# https://medium.com/data-hackers/como-manipular-planilhas-excel-com-o-python-6be8799f8dd7

class Campus(BaseModel):
    idCampus: str
    desc: str


class Local(BaseModel):
    idLocal: int
    desc: str
    idCampus: int

class Dados(BaseModel):
    campus: List[Campus]
    locais: List[Local]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/gerador_qts/")
async def gera_qts(dado: Dados):
    
    qtdCampus = len(dado.campus)
    qtdLocais = len(dado.locais)

    # Cria Novo workbook
    wb = Workbook()
    # Seleciona a active Sheet
    ws1 = wb.active
    # Rename it
    ws1.title = 'QTS'
            
    ws1['A1'] = 'Campus'
    # Colspan
    ws1.merge_cells('A1:B1')

    #Escreve alguns dados
    for col in range(1,3):
        for row in range(1,(qtdCampus+1)):
            letter = get_column_letter(col)
            ws1[letter + str(row+1)] = retorna_valor_campo(col,dado.campus[(row-1)])

    # Salva arquivo (Se não colocar o caminho complete, ele salva
    # na mesma pasta do scritp.

    wb.save('QTS.xlsx')

    return dado