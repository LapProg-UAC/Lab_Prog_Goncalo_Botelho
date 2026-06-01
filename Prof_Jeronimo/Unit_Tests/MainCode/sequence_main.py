import os
import yaml

# --- Configuration and Paths Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
# Check if YAML exists to avoid breaking during isolated test runs
if os.path.exists(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
else:
    config = None

OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")


def sequence(n):
    """
    Generates a list with the sequence f(i) = 3 * f(i-2) + f(i-1) for i >= 2.
    with base cases f(0) = 0 and f(1) = 1.
    
    Examples for doctest:
    >>> sequence(0)
    [0]
    >>> sequence(1)
    [0, 1]
    >>> sequence(5)
    [0, 1, 1, 4, 7, 19]
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("The argument 'n' must be a non-negative integer.")

    if n == 0:
        return [0]
    
    seq = [0, 1]  

    if n == 1:
        return seq
    
    for i in range(2, n + 1):
        next_val = 3 * seq[i-2] + seq[i-1]
        seq.append(next_val)

    return seq


def save_sequence_to_file(n, result, filepath):
    """Saves the generated sequence to a text file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("--- SEQUENCE GENERATOR REPORT ---\n")
        f.write(f"Target number (n): {n}\n")
        f.write(f"Generated Sequence: {result}\n")
    print(f"\nSuccess! The sequence was saved at:\n{filepath}")


def main():
    """Main execution pipeline."""
    if not config:
        print("Warning: config.yaml not found. Running with default value (19).")
        target_number = 19
        output_filename = "sequence_output.txt"
    else:
        target_number = config['sequence_parameters']['number_to_generate']
        output_filename = config['output_files']['sequence_result']

    try:
        print(f"Calculating sequence for n = {target_number}...")
        result = sequence(target_number)
        print(f"Result: {result}")
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        save_sequence_to_file(target_number, result, output_path)
        
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Run doctests automatically
    import doctest
    print("\n--- Running doctests ---")
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    main()