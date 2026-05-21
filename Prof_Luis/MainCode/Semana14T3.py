import os
import json
import sys
from typing import List, Dict, Any, Callable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")
PRESCRIPTIONS_FILE = os.path.join(OUTPUT_DIR, "prescriptions.json")


def get_patient(patients: List[Dict[str, Any]], condition: Callable[[Dict[str, Any]], bool]) -> Dict[str, Any]:
    """
    Uses higher-order functions (filter) to return a single patient from the list.
    """
    results = list(filter(condition, patients))
    return results[0] if results else None


def get_patients_by_id_range(patients: List[Dict[str, Any]], min_id: int, max_id: int) -> List[Dict[str, Any]]:
    """
    Uses higher-order functions (filter) to return a list of patients with an ID between min_id and max_id.
    """
    condition = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return list(filter(condition, patients))


def get_prescriptions_by_patient(patients: List[Dict[str, Any]], condition: Callable[[Dict[str, Any]], bool]) -> List[List[str]]:
    """
    Uses higher-order functions (map and filter) to return prescriptions associated with a specific patient.
    """
    return list(filter(None,map(lambda u: u["Prescribed_Medications"] if condition(u) else None, patients)))


def get_prescriptions_by_id_range(patients: List[Dict[str, Any]], min_id: int, max_id: int) -> List[List[str]]:
    """
    Uses higher-order functions to return prescriptions associated with patients whose IDs are between min_id and max_id.
    """
    condition = lambda u: min_id <= int(u["Patient_ID"].split("-")[1]) <= max_id
    return get_prescriptions_by_patient(patients, condition)


def main():
    """
    Main function that loads data from the ecosystem and demonstrates
    the practical usage of the 4 higher-order functions with clear outputs.
    """
    try:
        with open(PRESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            patients = data.get("Prescription", []) 
    except FileNotFoundError:
        print(f"[ERROR] The file '{PRESCRIPTIONS_FILE}' was not found.")
        print("Please make sure to run 'Semana4T2.py' first to generate the data.")
        sys.exit(1)

    if not patients:
        print("[WARNING] The patient list is empty.")
        return

    # --- Exercise 1 ---
    print("\nLooking for a patient with a specified ID ('U-00003'):")
    target_patient = get_patient(patients, lambda u: u["Patient_ID"] == "U-00003")
    if target_patient:
        print(f" -> [Success] Found: {target_patient['Patient_ID']} | Name: {target_patient['Patient_Name']}")
    else:
        print(" -> [Warning] Patient not found.")

    # --- Exercise 2 ---
    print("\nFilter patients with IDs in the range [2, 5]:")
    filtered_patients = get_patients_by_id_range(patients, 2, 5)
    for u in filtered_patients:
        print(f" -> {u['Patient_ID']} - {u['Patient_Name']}")

    # --- Exercise 3 ---
    print("\nGet the medical prescription for patient 'U-00003':")
    patient_prescription = get_prescriptions_by_patient(patients, lambda u: u["Patient_ID"] == "U-00003")
    if patient_prescription:
        print(f" -> Prescribed medications: {patient_prescription[0]}")
    else:
        print(" -> No prescription found for the given criteria.")

    # --- Exercise 4 ---
    print("\nGet all prescriptions for patients in the range [2, 5]:")
    range_prescriptions = get_prescriptions_by_id_range(patients, 2, 5)
    for index, prescription in enumerate(range_prescriptions):
        patient_id = filtered_patients[index]["Patient_ID"]
        print(f" -> {patient_id}: {prescription}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()