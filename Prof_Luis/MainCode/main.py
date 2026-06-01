import sys
import Semana3T1
import Semana4T2
import Semana14T3

def display_menu():
    print("\n" + "="*40)
    print("      MEDICAL SYSTEM PIPELINE      ")
    print("="*40)
    print("1. Generate Sinoptic Table (T1)")
    print("2. Generate Patient Prescriptions (T2)")
    print("3. Analyze Data with HOFs (T3)")
    print("0. Exit")
    print("="*40)

def main():
    while True:
        display_menu()
        choice = input("Select an option (0-3): ").strip()

        if choice == '1':
            Semana3T1.run()
        elif choice == '2':
            Semana4T2.run()
        elif choice == '3':
            Semana14T3.run()
        elif choice == '0':
            print("\nExiting system. Goodbye!")
            sys.exit(0)
        else:
            print("\n[ERROR] Invalid option. Please select a valid number.")

if __name__ == "__main__":
    main()