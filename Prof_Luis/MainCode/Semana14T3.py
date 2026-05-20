# --- Imports ---
import os
import json
import sys
from typing import List, Dict, Any, Callable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")
PRESCRIPTIONS_FILE = os.path.join(OUTPUT_DIR, "prescriptions.json")

def obter_utente(utentes: List[Dict[str, Any]], condicao: Callable[[Dict[str, Any]], bool]) -> Dict[str, Any]:
    """
    1. Usa funções de ordem superior (filter) para retornar um utente da lista de utentes.
    """
    resultados = list(filter(condicao, utentes))
    return resultados[0] if resultados else None


def obter_utentes_por_intervalo_id(utentes: List[Dict[str, Any]], min_id: int, max_id: int) -> List[Dict[str, Any]]:
    """
    2. Usa funções de ordem superior (filter) para retornar uma lista de utentes com o ID entre x e y.
    """
    condicao = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return list(filter(condicao, utentes))


def obter_receitas_por_utente(utentes: List[Dict[str, Any]], condicao: Callable[[Dict[str, Any]], bool]) -> List[List[str]]:
    """
    3. Usa funções de ordem superior (map e filter) para retornar as receitas associadas a um determinado utente.
    """
    return list(filter(None, map(lambda u: u["Prescribed_Medications"] if condicao(u) else None,utentes)))


def obter_receitas_por_intervalo_id(utentes: List[Dict[str, Any]], min_id: int, max_id: int) -> List[List[str]]:
    """
    4. Usa funções de ordem superior para retornar as receitas associadas aos utentes com o ID entre x e y.
    """
    condicao = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return obter_receitas_por_utente(utentes, condicao)


def Main():
    """
    Função principal que carrega os dados do ecossistema e demonstra
    o funcionamento prático das 4 funções de ordem superior com outputs claros.
    """
    try:
        with open(PRESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            utentes = dados.get("Prescription", [])
    except FileNotFoundError:
        print(f"[ERRO] O ficheiro '{PRESCRIPTIONS_FILE}' não foi encontrado.")
        print("Por favor, garante que executas o 'Semana4T2.py' primeiro para gerar os dados.")
        sys.exit(1)

    if not utentes:
        print("[AVISO] A lista de utentes está vazia.")
        return

    print("\n" + "="*60)
    print("   EXECUÇÃO E OUTPUTS DO MÓDULO: Semana14T3.py")
    print("="*60)

    # --- Exercício 1 ---
    print("\n[Exercício 1] À procura do utente com ID especificado ('U-00003'):")
    utente_alvo = obter_utente(utentes, lambda u: u["Patient_ID"] == "U-00003")
    if utente_alvo:
        print(f" -> [Sucesso] Encontrado: {utente_alvo['Patient_ID']} | Nome: {utente_alvo['Patient_Name']}")
    else:
        print(" -> [Aviso] Utente não encontrado.")

    # --- Exercício 2 ---
    print("\n[Exercício 2] Filtrar utentes com ID no intervalo [2, 5]:")
    utentes_filtrados = obter_utentes_por_intervalo_id(utentes, 2, 5)
    for u in utentes_filtrados:
        print(f" -> {u['Patient_ID']} - {u['Patient_Name']}")

    # --- Exercício 3 ---
    print("\n[Exercício 3] Obter a receita médica do utente 'U-00003':")
    receita_utente = obter_receitas_por_utente(utentes, lambda u: u["Patient_ID"] == "U-00003")
    if receita_utente:
        print(f" -> Medicamentos prescritos: {receita_utente[0]}")
    else:
        print(" -> Nenhuma receita encontrada para os critérios dados.")

    # --- Exercício 4 ---
    print("\n[Exercício 4] Obter todas as receitas dos utentes no intervalo [2, 5]:")
    receitas_intervalo = obter_receitas_por_intervalo_id(utentes, 2, 5)
    for index, receita in enumerate(receitas_intervalo):
        id_paciente = utentes_filtrados[index]["Patient_ID"]
        print(f" -> {id_paciente}: {receita}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    Main()