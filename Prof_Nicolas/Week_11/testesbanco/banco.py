from contabancaria import ContaBancaria


class Banco:
    """Representa um banco com uma coleção de contas."""

    def __init__(self):
        self.contas = {}

    def adicionar_conta(self, conta: ContaBancaria):
        """
        Adiciona uma conta ao banco.
        :param conta: Conta a ser adicionada.
        :return:
        """
        if conta.numero not in self.contas:
            self.contas[conta.numero] = conta

    def obter_conta(self, numero: int) -> ContaBancaria:
        """
        Pesquisa pela conta do banco a partir do número.
        :param numero: Número da conta pretendida.
        :return: Conta bancária com o número pretendido.
        """
        if numero in self.contas:
            return self.contas[numero]
        return None

    def transferir(self, numero_origem, numero_destino, valor) -> bool:
        """
        Transfere valor entre duas contas do banco, desde que as contas existam e a conta
        origem tenha saldo suficiente.
        :param numero_origem: Conta a partir da qual é feita a transferência.
        :param numero_destino: Conta que recebe o valor da transferência.
        :param valor:
        :return:
        """
        if numero_origem != numero_destino:
            origem = self.obter_conta(numero_origem)
            destino = self.obter_conta(numero_destino)
            if origem is not None and destino is not None:
                if origem.levantar(valor):
                    destino.depositar(valor)
                return True
        return False
