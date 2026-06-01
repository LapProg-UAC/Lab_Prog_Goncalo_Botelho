import os
import yaml

# --- Configuration and Paths Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

INPUT_DIR = os.path.join(BASE_DIR, "InputFiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def hash_folding_final(text, n=5):
    """Calculates the hash of a string using the folding method."""
    while len(text) % n != 0:
        text += str(n)

    blocks = []
    ascii_values = [ord(c) for c in text]
    for i in range(0, len(ascii_values), n):
        blocks.append(ascii_values[i:i+n])
    
    sums = [0] * n
    for block in blocks:
        for i in range(n):
            sums[i] += block[i]

    hash_list = [f"{(s % 256):02X}" for s in sums]
    
    return blocks, hash_list

def keyed_hash_final(text, key_list, n=5):
    """Generates a digital signature (keyed hash)."""
    blocks, base_hash = hash_folding_final(text, n)    

    signature = []
    for i in range(n):
        hash_value = int(base_hash[i], 16)
        key_value = key_list[i % len(key_list)]
        
        signature_sum = (hash_value + key_value) % 256
        signature.append(f"{signature_sum:02X}")
        
    return blocks, base_hash, signature

def calculate_file_hashes(input_path, output_path, key, n=5):
    """
    Processes a list of names from an input file, calculating their hashes
    and saving a formatted report to the output file.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()

        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write("HASHING AND AUTHENTICITY REPORT\n")
            f_out.write(f"Configuration: Hash length {n}\n\n")

            for line in lines:
                name = line.strip()
                if not name: 
                    continue

                blocks, integrity_hash, signature = keyed_hash_final(name, key, n)

                f_out.write(f"TEXT: {name}\n")
                f_out.write(f"BLOCKS: {blocks}\n")
                f_out.write(f"INTEGRITY HASH: {integrity_hash}\n")
                f_out.write(f"SIGNATURE (KEYED): {signature}\n\n")
        
        print(f"Success! The hash report was saved at:\n{output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Main execution pipeline."""
    secret_key = config['hashing_parameters']['secret_key']
    hash_len = config['hashing_parameters']['hash_length']
    
    input_filename = config['input_files']['names_list']
    output_filename = config['output_files']['hash_report']

    input_file_path = os.path.join(INPUT_DIR, input_filename)
    output_file_path = os.path.join(OUTPUT_DIR, output_filename)

    print("Processing file hashing...")
    calculate_file_hashes(input_file_path, output_file_path, secret_key, n=hash_len)

if __name__ == "__main__":
    main()