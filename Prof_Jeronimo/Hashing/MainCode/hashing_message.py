import os
import yaml

# --- Configuration Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')

with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

def hash_folding_final(text, n=5):
    """
    Calculates the hash of a string using the folding method.
    Pads the text with the string representation of 'n' if needed.
    """
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
    """
    Generates a digital signature (keyed hash) to prove data authenticity.
    """
    blocks, base_hash = hash_folding_final(text, n)
    
    signature = []
    for i in range(n):
        hash_value = int(base_hash[i], 16)
        key_value = key_list[i % len(key_list)]
        
        signature_sum = (hash_value + key_value) % 256
        signature.append(f"{signature_sum:02X}")
        
    return blocks, base_hash, signature

def main():
    """Main interactive execution."""
    secret_key = config['hashing_parameters']['secret_key']
    hash_len = config['hashing_parameters']['hash_length']

    message = str(input("Enter a message to hash: "))

    b, h, s = keyed_hash_final(message, secret_key, n=hash_len)

    print("\n--- Hashing Results ---")
    print(f"ASCII Blocks: {b}")
    print(f"Hash (Integrity): {h}")
    print(f"Signature (Authenticity): {s}")

if __name__ == "__main__":
    main()