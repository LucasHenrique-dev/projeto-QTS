from fastapi import FastAPI
from pydantic import BaseModel
import time
from typing import List
import random
import matplotlib.pyplot as plt


def converter_minutos(hora):
    t = time.strptime(hora, "%H:%M")
    minutos = t[3] * 60 + t[4]
    return minutos


def calcular_disciplinas_dia(horario, segmentacao_horario):
    inicio_aula, fim_aula = horario.horario_inicio, horario.horario_fim
    inicio_almoco, fim_almoco = horario.almoco.inicio, horario.almoco.fim
    duracao_dia = converter_minutos(fim_aula) - converter_minutos(inicio_aula)
    intervalo_almoco = converter_minutos(fim_almoco) - converter_minutos(inicio_almoco)
    return ((duracao_dia - intervalo_almoco) // segmentacao_horario) + 1


def calcular_horas_vagas(aulas):
    disciplinas = set(aulas)
    aula_vaga = 0

    for disciplina in disciplinas:
        if disciplina == 0:  # Ignora aulas vagas
            continue

        aula_atual = proxima_aula = 0
        while (
            aulas[proxima_aula:].count(disciplina) > 1
        ):  # Calcula horas vagas de uma disciplina
            aula_atual = aulas.index(disciplina, proxima_aula)
            proxima_aula = aulas.index(disciplina, aula_atual + 1)

            aula_vaga += proxima_aula - (aula_atual + 1)

    return aula_vaga


def calcular_restricao_3(aulas, gene_almoco):
    if aulas[gene_almoco - 1] == aulas[gene_almoco]:
        return 1

    return 0


class Almoco(BaseModel):
    inicio: str
    fim: str


class Horario(BaseModel):
    horario_inicio: str
    horario_fim: str
    duracao_hora_aula: int
    intervalo_minutos_entre_aulas: int
    almoco: Almoco
    dias_semana: List[str]


class Disciplina(BaseModel):
    nome: str
    restrição_horario: str
    sigla: str


class Curso(BaseModel):
    quantidade_turmas: int
    maximo_aulas_dia: int
    disciplinas: List[Disciplina]


class Data(BaseModel):
    curso: Curso
    horario: Horario


# comando para rodar : uvicorn main:app --reload

app = FastAPI()


@app.post("/gerador_qts/")
async def gera_qts(data: Data):
    # name_days_week = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

    dias_semana = data.horario.dias_semana

    disciplinas = {0: ("NA", "Horário Vago")}

    for index, disciplina in enumerate(data.curso.disciplinas):
        disciplinas[index + 1] = (disciplina.sigla, disciplina.nome)

    hora_aula = data.horario.duracao_hora_aula * 60
    intervalo_aula = data.horario.intervalo_minutos_entre_aulas

    segmentacao_horario = (
        hora_aula + intervalo_aula
    )  # Divisão do horário no QTS (minutos)
    espacos_totais = calcular_disciplinas_dia(
        data.horario, segmentacao_horario
    )  # Retorna quantidade de sessões destinadas às disciplinas pela manhã

    inicio_aula = converter_minutos(data.horario.horario_inicio)
    inicio_almoco = converter_minutos(data.horario.almoco.inicio)
    aulas_manha = (
        ((inicio_almoco - inicio_aula) // segmentacao_horario) + 1
    ) // data.curso.maximo_aulas_dia
    gene_almoco = aulas_manha  # Gene inicial é o zero!

    disciplinas_dia = espacos_totais // data.curso.maximo_aulas_dia

    dominio = [(0, len(disciplinas) - 1)] * (
        data.curso.quantidade_turmas * len(dias_semana) * disciplinas_dia
    )

    def gerar_cromossomo(
        turmas=data.curso.quantidade_turmas,
        qtd_dias_semana=len(dias_semana),
        disciplinas_dia=disciplinas_dia,
        dominio=dominio[0],
    ):
        tamanho_cromossomo = turmas * qtd_dias_semana * disciplinas_dia
        cromossomo = []

        for i in range(tamanho_cromossomo):
            cromossomo += [random.randint(dominio[0], dominio[1])]

        return cromossomo

    constante_objetivo = 10

    def avaliar_objetivos(aulas_dia):
        desvio = 0

        desvio += calcular_horas_vagas(aulas_dia)  # Objetivo 1

        return constante_objetivo * desvio

    def aplicar_penalidades(aulas_dia):
        desvio, constante = 0, 100

        desvio += calcular_restricao_3(aulas_dia, gene_almoco)  # Restrição 3

        return constante * desvio

    def funcao_avaliacao(calendario):
        pontuacao = 0

        for i in range(0, len(calendario), disciplinas_dia):
            aulas_dia = calendario[i : i + disciplinas_dia]

            pontuacao += avaliar_objetivos(
                aulas_dia
            )  # Pontuar pelo nível de cumprimento dos objetivos
            pontuacao += aplicar_penalidades(
                aulas_dia
            )  # Penalizar descumprimento das restrições

        return pontuacao

    def imprimir_qts(individuo):
        dia_id = 0
        espera_total = 0
        qtd_dias_semana = len(dias_semana)
        dados_qts = {}
        for i in range(data.curso.quantidade_turmas):
            inicio_turma = i * (disciplinas_dia * qtd_dias_semana)
            dados_dia = {}
            for j in range(qtd_dias_semana):
                dia = dias_semana[j]
                comeco_semana = inicio_turma + j * disciplinas_dia

                disciplinas_semana = individuo[
                    comeco_semana : comeco_semana + disciplinas_dia
                ]  # coleta as disciplinas da semana
                expandir_grupos = [
                    info
                    for aula in disciplinas_semana
                    for info in [aula] * data.curso.maximo_aulas_dia
                ]  # expõem a quantidade real de aulas
                decodificar_disciplinas = [
                    disciplinas[disciplina][0] for disciplina in expandir_grupos
                ]  # traduz números em disciplinas

                decodificar_disciplinas.insert(
                    gene_almoco * data.curso.maximo_aulas_dia, "Almoço"
                )  # inserção do horário de almoço

                dados_dia[dia] = {", ".join(decodificar_disciplinas)}

                dia_id += 1  # próximo dia da semana
                espera_total += (
                    avaliar_objetivos(disciplinas_semana) // constante_objetivo
                ) * data.curso.maximo_aulas_dia
            dados_qts[i + 1] = dados_dia

        dados_qts["espera_total"] = espera_total
        return dados_qts

    individuo = gerar_cromossomo()

    def mutacao(passo, calendario, probabilidade, dominio=dominio):
        gene = random.randint(
            0, len(dominio) - 1
        )  # Escolha do gene que sofrerá a mutação
        mutante = calendario

        # Joga um número aleatório para verificar se haverá mutação.
        if random.random() < probabilidade:
            if calendario[gene] != dominio[gene][0]:  # Verifica borda inferior
                mutante = (
                    calendario[0:gene]
                    + [calendario[gene] - passo]
                    + calendario[gene + 1 :]
                )
            elif calendario[gene] != dominio[gene][1]:  # Verifica borda superior
                mutante = (
                    calendario[0:gene]
                    + [calendario[gene] + passo]
                    + calendario[gene + 1 :]
                )
        return mutante

    def crossover(individuo1, individuo2, dominio=dominio):
        gene = random.randint(1, len(dominio) - 2)

        return individuo1[0:gene] + individuo2[gene:]

    def algoritmo_genetico(
        tamanho_populacao=10,
        passo=1,
        elitismo=0.2,
        numero_geracoes=100,
        probabilidade_mutacao=0.05,
        dominio=dominio,
    ):
        populacao = []
        for i in range(tamanho_populacao):
            # Cria aleatoriamente os indivíduos
            individuo = gerar_cromossomo()
            populacao.append(individuo)

        numero_elitismo = int(elitismo * tamanho_populacao)

        melhor_fit = []  # Guardar o melhor de cada interação

        for i in range(numero_geracoes):
            custos = [
                (funcao_avaliacao(individuo), individuo) for individuo in populacao
            ]

            custos.sort()

            individuos_ordenados = [individuo for (custo, individuo) in custos]

            populacao = individuos_ordenados[
                0:numero_elitismo
            ]  # só pega o percentual dos elementos baseados no elisitmo

            while len(populacao) < tamanho_populacao:
                i1 = random.randint(0, numero_elitismo)
                i2 = random.randint(0, numero_elitismo)

                novo_individuo = crossover(
                    individuos_ordenados[i1], individuos_ordenados[i2]
                )

                mutacao_novo_individuo = mutacao(
                    passo, novo_individuo, probabilidade_mutacao
                )

                populacao.append(mutacao_novo_individuo)

            melhor_fit.append(custos[0][0])

        # Plotar o gráfico
        plt.plot(melhor_fit)

        return custos[0][1]

    solucao = algoritmo_genetico(tamanho_populacao=10, numero_geracoes=400)

    qts = imprimir_qts(solucao)
    qts["avaliacao"] = funcao_avaliacao(solucao)

    return qts
