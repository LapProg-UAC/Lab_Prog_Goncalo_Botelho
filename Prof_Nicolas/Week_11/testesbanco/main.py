from UI import mostrar_menu, opcao_adicionar_conta, opcao_transferir, opcao_listar_contas
from banco import Banco


def executar_app():
    banco = Banco()

    while True:
        mostrar_menu()
        opcao = input("Opção: ")
        if opcao == "1":
            opcao_adicionar_conta(banco)
        elif opcao == "2":
            opcao_transferir(banco)
        elif opcao == "3":
            opcao_listar_contas(banco)
        elif opcao == "0":
            print("A terminar...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    executar_app()
