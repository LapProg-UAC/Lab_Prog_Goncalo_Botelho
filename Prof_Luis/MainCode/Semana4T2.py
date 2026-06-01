import os
import openpyxl
import json
import random
import sys
import yaml
from typing import Dict, List, Tuple

# --- Configuration Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

INPUT_DIR = os.path.join(BASE_DIR, "InputFiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

EXCEL_FILE = os.path.join(OUTPUT_DIR, config['files']['outputs']['sinoptic_table'])
NAMES_FILE = os.path.join(INPUT_DIR, config['files']['inputs']['names'])
SURNAMES_FILE = os.path.join(INPUT_DIR, config['files']['inputs']['surnames'])
OUTPUT_FILE = os.path.join(OUTPUT_DIR, config['files']['outputs']['prescriptions'])

PATIENTS_NUM = config['t2_parameters']['patients_num']
MIN_MEDS = config['t2_parameters']['min_meds']
MAX_MEDS = config['t2_parameters']['max_meds']
INTERACTION_LIMIT = config['t2_parameters']['interaction_limit']

INTERACTIONS_MAPPING: Dict[int, str] = {
    0: "No clinical significance",
    1: "Potentially serious",
    2: "Enhancer of therapeutic/toxic effect (horizontal column)",
    3: "Enhancer of therapeutic/toxic effect (vertical column)",
    4: "Decreases therapeutic/toxic effect (horizontal column)",
    5: "Decreases therapeutic/toxic effect (vertical column)",
}

# --- Functions ---
def normalize_name(name: str) -> str:
    return str(name).strip().lower() if name else ""

def read_file(path: str, encoding: str = "utf-8") -> List[str]:
    try:
        with open(path, "r", encoding=encoding) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] File '{path}' not found.")
        return []

def read_excel(path: str) -> Tuple[List[str], Dict]:
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.active

        original_names = []
        for col in range(2, ws.max_column + 1):
            val = ws.cell(row=1, column=col).value
            if val:
                original_names.append(str(val))

        table = {}
        for row in range(2, ws.max_row + 1):
            line_name = ws.cell(row=row, column=1).value
            if not line_name: continue
            
            key_line = normalize_name(line_name)
            table[key_line] = {}

            for col_idx, name_col in enumerate(original_names, start=2):
                key_col = normalize_name(name_col)
                val_cell = ws.cell(row=row, column=col_idx).value
                table[key_line][key_col] = int(val_cell) if val_cell is not None else 0
                
        return original_names, table
    except FileNotFoundError:
        print(f"[ERROR] '{path}' not found. Please run Module T1 first!")
        return [], {}

def calculate_balance(prescription: List[str], table: Dict) -> Dict:
    interactions = []
    count = {str(v): 0 for v in range(6)}
    
    n = len(prescription)
    for i in range(n):
        for j in range(i + 1, n):
            med_a, med_b = prescription[i], prescription[j]
            v = table.get(normalize_name(med_a), {}).get(normalize_name(med_b), 0)
            count[str(v)] += 1
            interactions.append({
                "Medicine_a": med_a,
                "Medicine_b": med_b,
                "Value": v,
                "Description": INTERACTIONS_MAPPING.get(v, "Unknown")
            })

    has_interactions = any(p["Value"] >= INTERACTION_LIMIT for p in interactions)
    return {
        "Analyzed_Pairs": len(interactions),
        "Interactions": sorted(interactions, key=lambda x: x["Value"], reverse=True),
        "Count_by_Type": count,
        "Have_Interactions": has_interactions,
        "Decision": "With Interactions" if has_interactions else "Without Interactions"
    }

def run(encoding: str = "utf-8") -> None:
    print("\n--- Running Module T2 (Prescription Generator) ---")
    meds, table = read_excel(EXCEL_FILE)
    if not meds: return

    names = read_file(NAMES_FILE)
    surnames = read_file(SURNAMES_FILE)
    if not names or not surnames: return

    prescriptions = []
    for i in range(PATIENTS_NUM):
        patient_name = f"{random.choice(names)} {random.choice(surnames)}"
        meds_num = random.randint(MIN_MEDS, min(MAX_MEDS, len(meds)))
        meds_list = random.sample(meds, meds_num)
        
        balance = calculate_balance(meds_list, table)
        
        prescriptions.append({
            "Patient_ID": f"U-{i+1:05d}",
            "Patient_Name": patient_name,
            "Prescribed_Medications": meds_list,
            "Num_Medicines": len(meds_list),
            "Balance_Interactions": balance
        })

    with open(OUTPUT_FILE, "w", encoding=encoding) as f:
        json.dump({"Total_Patients": len(prescriptions), "Prescription": prescriptions}, f, ensure_ascii=False, indent=4)
    
    print(f"[OK] Generated {len(prescriptions)} Prescriptions in '{os.path.basename(OUTPUT_FILE)}'.")

if __name__ == "__main__":
    run()