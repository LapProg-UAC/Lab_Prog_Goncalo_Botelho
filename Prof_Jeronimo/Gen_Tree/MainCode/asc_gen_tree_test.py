import os
import yaml
from asc_gen_tree import AscGenTree

# --- Configuration and Paths Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

yaml_path = os.path.join(CURRENT_DIR, 'config.yaml')
with open(yaml_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

INPUT_DIR = os.path.join(BASE_DIR, "InputFiles")
OUTPUT_DIR = os.path.join(BASE_DIR, "OutputFiles")

# Ensure Output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main() -> None:
    """
    Main function to test the ascending genealogical tree implementation.
    Loads data from an input file, runs queries based on config, and saves a report.
    It gives the person on the root, the parents of a specific person, and the maternal and paternal ancestors of two different people.
    """
    agt = AscGenTree() 
    
    input_filename = config['input_files']['family_data']
    data_path = os.path.join(INPUT_DIR, input_filename)
    agt.load_from_file(data_path)
    
    output_filename = config['output_files']['genealogy_report']
    report_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(report_path, 'w', encoding='utf-8') as report:
        report.write("--- GENEALOGICAL TREE REPORT ---\n\n")

        # Base Tree Check
        if agt.get_root():
            root_msg = f"Person at the root of the tree: {agt.get_root().get_name()}\n"
            print(f"\n{root_msg.strip()}")
            report.write(root_msg)
            report.write("=" * 60 + "\n")
            print("=" * 60)

        # Parents
        search_parents = config['queries']['person_parents']
        parents = agt.get_parents(search_parents)
        
        p_msg = f"Parents of {search_parents}: {parents}\n"
        print(p_msg.strip())
        report.write(p_msg)
        report.write("=" * 60 + "\n")
        print("=" * 60)

        # Maternal Ancestors
        q1 = config['queries']['ancestor_search_1']
        maternal_ancs = agt.get_ancestors(q1['person'], q1['degree'], q1['side'])
        
        m_msg = f"{q1['side'].capitalize()} Ancestors of {q1['person']} (Degree {q1['degree']}): {maternal_ancs}\n"
        print(m_msg.strip())
        report.write(m_msg)
        report.write("=" * 60 + "\n")
        print("=" * 60)

        # Paternal Ancestors
        q2 = config['queries']['ancestor_search_2']
        paternal_ancs = agt.get_ancestors(q2['person'], q2['degree'], q2['side'])
        
        pat_msg = f"{q2['side'].capitalize()} Ancestors of {q2['person']} (Degree {q2['degree']}): {paternal_ancs}\n"
        print(pat_msg.strip())
        report.write(pat_msg)
        report.write("=" * 60 + "\n")

    print(f"\nSuccess! The report '{output_filename}' was generated at:\n{report_path}\n")

if __name__ == "__main__":
    main()