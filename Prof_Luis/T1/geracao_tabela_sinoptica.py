import random 
import sys
import openpyxl

def read_file(path):
    try:
        with open(path, 'r', encoding = 'utf-8') as file:
            
            meds = [line.strip() for line in file if line.strip()]

            if not meds:
                raise ValueError("The file is empty")
            return meds
        
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def generate_synoptic_table(meds):
    size = len(meds)
    matrix = []

    for line_idx in range(size):
        actual_line = []
        for column_idx in range (size):
            if line_idx == column_idx:
                actual_line.append(0)
            else:
                actual_line.append(random.randint(0, 6))
        matrix.append(actual_line)
    return matrix

def save_to_excel(matrix, meds, output_path):

    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Interações Medicamentosas'
        
        # Write headers
        header = ['Medicamentos'] + meds
        sheet.append(header)

        # Write data rows
        for i, meds in enumerate (meds):
            row = [meds] + matrix[i]
            sheet.append(row)

        workbook.save(output_path)
        print(f"Synoptic table saved to '{output_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving to Excel: {e}")
        sys.exit(1)

def save_to_txt(matrix, meds, output_path):
    try:
        with open(output_path, 'w', encoding = 'utf-8') as file:
            #size = len(meds)
            # definir o tamanho da coluna com base no medicamento mais longo
            size = max(len(med) for med in meds) + 2

            header = " " * size
            for med in meds:
                # alinha o texto mais á direita com >
                header += f"{med:>{size}}"
            file.write(header + "\n")

            for i, med in enumerate(meds):
                row = f"{med:<{size}}"  # alinha o texto mais à esquerda com <
                for value in matrix[i]:
                    row += f"{value:>{size}}"  # alinha os valores mais à direita com >
                file.write(row + "\n")

        print(f"Synoptic table saved to '{output_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving to text file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3 or not sys.argv[1] or not sys.argv[2]:
        print("Error: No input file or output file provided.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] 

    meds = read_file(input_path + '.txt')
    matrix = generate_synoptic_table(meds)
    save_to_excel(matrix, meds, output_path + '.xlsx')
    save_to_txt(matrix, meds, output_path + '.txt')

if __name__ == "__main__":
    main()
