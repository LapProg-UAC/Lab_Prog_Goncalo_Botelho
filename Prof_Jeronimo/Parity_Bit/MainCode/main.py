import os
import random
import yaml
from datetime import datetime

# --- Configuration and Paths Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

# Load YAML configuration
yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

# Ensure Output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def calculate_even_parity(n):
    """Calculates the even parity bit."""
    return bin(n).count('1') % 2

def flip_random_bit(n):
    """Inverts a random bit in a 7-bit number (0-127)."""
    position = random.randint(0, 6)
    return n ^ (1 << position)

def main():
    """Main execution pipeline for parity check simulation."""
    random.seed(datetime.now().timestamp())

    min_rec = config['simulation_parameters']['min_records']
    max_rec = config['simulation_parameters']['max_records']
    err_divider = config['simulation_parameters']['error_ratio_divider']
    report_filename = config['output_files']['final_report']

    num_records = random.randint(min_rec, max_rec)
    
    processed_data = []
    detected_errors_list = []
    
    original_numbers = [random.randint(0, 127) for _ in range(num_records)]
    
    error_indices = random.sample(range(num_records), num_records // err_divider)

    for i in range(num_records):
        n_orig = original_numbers[i]
        p1 = calculate_even_parity(n_orig)
        
        if i in error_indices:
            n_received = flip_random_bit(n_orig)
        else:
            n_received = n_orig
            
        p2 = calculate_even_parity(n_received)
        has_error = (p1 != p2)
        
        if has_error:
            detected_errors_list.append(i + 1) 
            
        processed_data.append({
            'num': n_orig,
            'p1': p1,
            'p2': p2,
            'status': "INVALID" if has_error else "OK"
        })
    
    if detected_errors_list:
        print(f"ERRORS DETECTED at indices: {detected_errors_list}")
        print(f"Total failures: {len(detected_errors_list)}")
    else:
        print("No errors detected.")

    report_path = os.path.join(OUTPUT_DIR, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Total records: {num_records}\n\n")
        f.write(f"{'Index':^8} | {'Number':^8} | {'Parity 1':^12} | {'Parity 2':^12} | {'Status':^8}\n")
        
        for idx, item in enumerate(processed_data):
            f.write(f"{idx+1:^8} | {item['num']:^8} | {item['p1']:^12} | {item['p2']:^12} | {item['status']:^8}\n")
        
        if detected_errors_list:
            f.write(f"\nSUMMARY: Errors were found at indices: {detected_errors_list}\n")
        else:
            f.write("\nSUMMARY: All parity bits are correct.\n")

    print(f"\nSuccess! The report '{report_filename}' was generated at:\n{report_path}")

if __name__ == "__main__":
    main()