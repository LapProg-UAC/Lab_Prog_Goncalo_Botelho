def sequence(n):
    """
    Gera uma lista com a sequência f(i) = 3 * f(i-2) + f(i-1) para i >= 2.
    com f(0) = 0 e f(1) = 1.
    
    Exemplos para doctest:
    >>> sequence(0)
    [0]
    >>> sequence(1)
    [0, 1]
    >>> sequence(5)
    [0, 1, 1, 4, 7, 19]
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("O argumento n deve ser um número inteiro não negativo.")

    if n == 0:
        return [0]
    
    seq = [0, 1]  

    if n == 1:
        return seq
    
    for i in range(2, n + 1):
        next_val = 3 * seq[i-2] + seq[i-1]
        seq.append(next_val)

    return seq

if __name__ == "__main__":
    try:
        n = int(input("Digite um número inteiro não negativo: "))
        result = sequence(n)
        print(result)
    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    import doctest
    print("\nExecutando testes doctest...")
    doctest.testmod(verbose=True)