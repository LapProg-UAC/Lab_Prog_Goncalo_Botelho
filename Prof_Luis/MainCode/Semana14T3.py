import os
import json
import yaml
from typing import List, Dict, Any, Callable

# --- Configuration Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")
os.makedirs(OUTPUT_DIR, exist_ok=True) # Garante que a pasta existe

PRESCRIPTIONS_FILE = os.path.join(OUTPUT_DIR, config['files']['outputs']['prescriptions'])
REPORT_FILE = os.path.join(OUTPUT_DIR, config['files']['outputs']['t3_report'])

TARGET_ID = config['t3_parameters']['target_patient_id']
MIN_ID = config['t3_parameters']['min_id_range']
MAX_ID = config['t3_parameters']['max_id_range']

# --- Higher-Order Functions ---
def get_patient(patients: List[Dict[str, Any]], condition: Callable[[Dict[str, Any]], bool]) -> Dict[str, Any]:
    results = list(filter(condition, patients))
    return results[0] if results else None

def get_patients_by_id_range(patients: List[Dict[str, Any]], min_id: int, max_id: int) -> List[Dict[str, Any]]:
    condition = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return list(filter(condition, patients))

def get_prescriptions_by_patient(patients: List[Dict[str, Any]], condition: Callable[[Dict[str, Any]], bool]) -> List[List[str]]:
    return list(filter(None, map(lambda u: u["Prescribed_Medications"] if condition(u) else None, patients)))

def get_prescriptions_by_id_range(patients: List[Dict[str, Any]], min_id: int, max_id: int) -> List[List[str]]:
    condition = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return get_prescriptions_by_patient(patients, condition)

def run():
    print("\n--- Running Module T3 (Higher-Order Functions Analysis) ---")
    try:
        with open(PRESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            patients = data.get("Prescription", []) 
    except FileNotFoundError:
        print(f"[ERROR] The file '{os.path.basename(PRESCRIPTIONS_FILE)}' was not found.")
        print("Please run Module T2 first to generate the data.")
        return

    if not patients:
        print("[WARNING] The patient list is empty.")
        return

    # Lista para acumular o texto que vai para a consola e para o ficheiro
    report_lines = []
    report_lines.append("=== HIGHER-ORDER FUNCTIONS ANALYSIS REPORT ===")

    # --- Analysis Execution using YAML config variables ---
    report_lines.append(f"\nLooking for patient with ID '{TARGET_ID}':")
    target_patient = get_patient(patients, lambda u: u["Patient_ID"] == TARGET_ID)
    if target_patient:
        report_lines.append(f" -> [Success] Found Name: {target_patient['Patient_Name']}")
    else:
        report_lines.append(" -> [Warning] Patient not found.")

    report_lines.append(f"\nFilter patients with IDs in the range [{MIN_ID}, {MAX_ID}]:")
    filtered_patients = get_patients_by_id_range(patients, MIN_ID, MAX_ID)
    for u in filtered_patients:
        report_lines.append(f" -> {u['Patient_ID']} - {u['Patient_Name']}")

    report_lines.append(f"\nGet the medical prescription for patient '{TARGET_ID}':")
    patient_prescription = get_prescriptions_by_patient(patients, lambda u: u["Patient_ID"] == TARGET_ID)
    if patient_prescription:
        report_lines.append(f" -> Prescribed medications: {patient_prescription[0]}")
    else:
        report_lines.append(" -> No prescription found.")

    report_lines.append(f"\nGet all prescriptions for patients in the range [{MIN_ID}, {MAX_ID}]:")
    range_prescriptions = get_prescriptions_by_id_range(patients, MIN_ID, MAX_ID)
    for index, prescription in enumerate(range_prescriptions):
        patient_id = filtered_patients[index]["Patient_ID"]
        report_lines.append(f" -> {patient_id}: {prescription}")

    report_lines.append("\n" + "="*60)

    # 1. Imprimir tudo na consola
    for line in report_lines:
        print(line)

    # 2. Guardar tudo no ficheiro de relatório
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"\n[OK] Analysis report successfully saved to: '{os.path.basename(REPORT_FILE)}'.")

if __name__ == "__main__":
    run()