from banco import Banco
from contabancaria import ContaBancaria


def mostrar_menu():
    print("\n=== BANCO ===")
    print("1 - Adicionar conta")
    print("2 - Transferir")
    print("3 - Listar contas")
    print("0 - Sair")


def opcao_adicionar_conta(banco: Banco):
    numero = int(input("Número da conta: "))
    titular = input("Titular: ")
    saldo = float(input("Saldo inicial: "))
    conta = ContaBancaria(numero, titular, saldo)
    banco.adicionar_conta(conta)
    print("Conta adicionada com sucesso.")


def opcao_transferir(banco: Banco):
    origem = int(input("Conta origem: "))
    destino = int(input("Conta destino: "))
    valor = float(input("Valor: "))
    if banco.transferir(origem, destino, valor):
        print("Transferência realizada com sucesso.")
    else:
        print("Transferência falhou.")


def opcao_listar_contas(banco: Banco):
    if len(banco.contas) == 0:
        print("Sem contas registadas.")
    for numero, conta in banco.contas.items():
        print(f"{numero} - {conta.titular} - {conta.saldo}")
