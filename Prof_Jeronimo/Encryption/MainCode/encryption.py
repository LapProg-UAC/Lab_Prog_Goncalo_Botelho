import os

def encrypt(text, key):
    """Encrypts text by shifting the ASCII value of each character."""
    result = ""
    if isinstance(key, int):
        key = [key]
    for i, char in enumerate(text):
        ascii_val = ord(char)
        k = key[i % len(key)]
        new_val = (ascii_val + k) % 128
        result += chr(new_val)
    return result

def decrypt(text, key):
    """Decrypts text by subtracting the key from the ASCII value."""
    result = ""
    if isinstance(key, int):
        key = [key]
    for i, char in enumerate(text):
        ascii_val = ord(char)
        k = key[i % len(key)]
        new_val = (ascii_val - k) % 128
        result += chr(new_val)
    return result

def encrypt_file(input_file, output_file, key):
    """Reads a text file, encrypts its content, and saves it to a new file."""
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    encrypted_text = encrypt(text, key)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encrypted_text)

def decrypt_file(input_file, output_file, key):
    """Decrypts a previously encrypted file."""
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted_text = decrypt(text, key)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decrypted_text)

def encrypt_field(input_file, output_file, key, field_index):
    """Encrypts only a specific field in a semicolon-separated file."""
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            fields = line.strip().split(";")
            if field_index < len(fields):
                fields[field_index] = encrypt(fields[field_index], key)
            new_line = ";".join(fields)
            f.write(new_line + "\n")

def save_txt(encrypted_text, decrypted_text, output_dir):
    """Saves the interactive encryption log."""
    filepath = os.path.join(output_dir, "encrypted_message.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Encrypted text: " + encrypted_text + "\n")
        f.write("Decrypted text: " + decrypted_text + "\n")
    print(f"\nLog successfully saved at: {filepath}\n")

def main():
    text_to_encrypt = input("Enter a message to encrypt: ")
    key = []
    multiple_keys = input("Do you want to use multiple keys? (y/n): ").lower()
    
    if multiple_keys == "n":
        key_input = int(input("Enter the key: "))
        key.append(key_input)
    elif multiple_keys == "y":
        for i in range(len(text_to_encrypt)//2):
            key_input = int(input(f"Enter key {i+1}: "))
            key.append(key_input)

    encrypted_text = encrypt(text_to_encrypt, key)
    decrypted_text = decrypt(encrypted_text, key)
    
    # --- Path Definition for OutputFiles ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    output_dir = os.path.join(base_dir, "OutputFiles")
    
    os.makedirs(output_dir, exist_ok=True)
    
    save_txt(encrypted_text, decrypted_text, output_dir)

    print("Original text:", text_to_encrypt)
    print("Encrypted:", encrypted_text)
    print("Decrypted:", decrypted_text)
    
    if text_to_encrypt == decrypted_text:
        print("Verification: OK")
    else:
        print("Error during decryption")

if __name__ == "__main__":  
    main()