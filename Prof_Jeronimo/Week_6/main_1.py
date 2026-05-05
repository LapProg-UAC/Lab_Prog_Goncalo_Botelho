def hash_folding_final(texto, n=5):
    """
    Calcula o hash de uma string utilizando o método de folding.
    
    O texto é dividido em blocos de tamanho 'n'. Se necessário, é aplicado 
    um preenchimento com o algarismo correspondente ao valor de 'n' 
    para garantir que o texto é múltiplo do comprimento do hash.

    Args:
        texto (str): A string original ou conteúdo do ficheiro a processar.
        n (int): O comprimento fixo do hash pretendido.

    Returns:
        tuple: Uma lista de listas (blocos ASCII) e uma lista de strings hexadecimais.
    """

    while len(texto) % n != 0:
        texto += str(n)

    blocos = []
    ascii_values = [ord(c) for c in texto]
    for i in range(0, len(ascii_values), n):
        blocos.append(ascii_values[i:i+n])
    
    somas = [0] * n
    for bloco in blocos:
        for i in range(n):
            somas[i] += bloco[i]

    hash_lista = [f"{(s % 256):02X}" for s in somas]
    
    return blocos, hash_lista

def keyed_hash_final(texto, chave_lista, n=5):
    """
    Gera uma assinatura digital (keyed hash) para comprovar a autenticidade dos dados.
    
    Adiciona uma sequência de números ao valor obtido pelo método folding,
    utilizando a aritmética de resto da divisão por 256.

    Args:
        texto (str): A mensagem a ser assinada.
        chave_lista (list): Lista de inteiros (0-255) usada como chave secreta.
        n (int): Comprimento do hash.

    Returns:
        tuple: Blocos ASCII, Hash de integridade e Assinatura de autenticidade.
    """

    blocos, h_base = hash_folding_final(texto, n)    

    assinatura = []
    for i in range(n):
        valor_hash = int(h_base[i], 16)

        valor_chave = chave_lista[i % len(chave_lista)]
        
        soma_assinatura = (valor_hash + valor_chave) % 256
        assinatura.append(f"{soma_assinatura:02X}")
        
    return blocos, h_base, assinatura

def calcular_hashes_ficheiro(caminho_entrada, caminho_saida, chave, n=5):
    """
    Processa um ficheiro de nomes, guardando o hash e a estrutura de blocos 
    para documentação e depuração.
    """
    try:
        with open(caminho_entrada, 'r', encoding='utf-8') as f_in:
            linhas = f_in.readlines()

        with open(caminho_saida, 'w', encoding='utf-8') as f_out:
            f_out.write("RELATÓRIO DE HASHING E AUTENTICIDADE\n")
            f_out.write(f"Configuração: Hash de comprimento {n}\n\n")

            for linha in linhas:
                nome = linha.strip()
                if not nome: continue

                blocos, h_integridade, assinatura = keyed_hash_final(nome, chave, n)

                f_out.write(f"TEXTO: {nome}\n")
                
                f_out.write(f"BLOCKS: {blocos}\n")
                
                f_out.write(f"HASH INTEGRIDADE: {h_integridade}\n")
                f_out.write(f"SIGNATURE (KEYED): {assinatura}\n\n")
        
        print(f"Sucesso! Verifica o ficheiro '{caminho_saida}' para veres os blocos.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

minha_chave_secreta = [10, 20, 30, 40, 50]
ficheiro = str(input("Indique o nome do ficheiro: "))

def main():
    calcular_hashes_ficheiro(ficheiro+'.txt', 'resultados.txt', minha_chave_secreta)

#if __name__ == "__main_1__":
main()