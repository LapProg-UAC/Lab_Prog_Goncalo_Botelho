import os
import openpyxl
import random
import sys
import yaml
from typing import List

# --- Configuration Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

INPUT_DIR = os.path.join(BASE_DIR, "InputFiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MEDS_FILE = os.path.join(INPUT_DIR, config['files']['inputs']['medications']) 
OUTPUT_FILE = os.path.join(OUTPUT_DIR, config['files']['outputs']['sinoptic_table'])

MIN_VALUE = config['t1_parameters']['min_interaction_value']
MAX_VALUE = config['t1_parameters']['max_interaction_value']

def read_meds(file_path: str, encoding: str = "utf-8") -> List[str]:
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] The file '{file_path}' was not found.")
        return []

def generate_sinoptic_table(meds: List[str]) -> List[List[int]]:
    n = len(meds)
    return [[0 if i == j else random.randint(MIN_VALUE, MAX_VALUE) for j in range(n)] for i in range(n)]

def save_to_excel(meds: List[str], table: List[List[int]], output_file: str) -> None:
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Interactions"

        for col_idx, name in enumerate(meds, start=2):
            ws.cell(row=1, column=col_idx, value=name)

        for row_idx, med_name in enumerate(meds, start=2):
            ws.cell(row=row_idx, column=1, value=med_name)
            for col_idx, val in enumerate(table[row_idx-2], start=2):
                ws.cell(row=row_idx, column=col_idx, value=val)

        wb.save(output_file)
        print(f"[OK] Excel File '{os.path.basename(output_file)}' generated successfully.")
    except Exception as e:
        print(f"[ERROR] Saving Excel file: {e}")

def run():
    print("\n--- Running Module T1 (Sinoptic Table) ---")
    meds = read_meds(MEDS_FILE)
    if not meds: 
        return
    
    table = generate_sinoptic_table(meds)
    save_to_excel(meds, table, OUTPUT_FILE)

if __name__ == "__main__":
    run()