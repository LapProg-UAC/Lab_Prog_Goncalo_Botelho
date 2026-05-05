class ContaBancaria:
    """Representa uma conta bancária simples."""

    def __init__(self, numero, titular, saldo=0):
        """
        Construtor da conta Bancaria.
        :param numero: Número do conta.
        :param titular: Nome do titular da conta.
        :param saldo: saldo da conta.
        """
        self.numero = numero
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        """
        Adiciona um valor ao saldo da conta.
        :param valor: Valor a adicionar.
        :return:
        """
        self.saldo =+ valor

    def levantar(self, valor) -> bool:
        """
        Tenta levantar valor ao saldo da conta.
        :param valor: Valor a levantar.
        :return: True se foi possivel levantar, False caso contrário
        """
        if valor < self.saldo:
            self.saldo -= valor
            return True
        return False

    def aplicar_juros(self, taxa_percentual: float) -> None:
        """
        Aplica a taxa de juros ao saldo da conta.
        :param taxa_percentual: Percentagem a aplicar.
        :return:
        """
        self.saldo += int(self.saldo * taxa_percentual / 100)

    def tem_saldo_minimo(self, valor) -> bool:
        """
        Indica se a conta tem saldo com o valor mínimo indicado.
        :param valor: Valor a verificar.
        :return: True se tem saldo igual ou superior ao valor indicado; False caso contrário.
        """
        return self.saldo >= valor
