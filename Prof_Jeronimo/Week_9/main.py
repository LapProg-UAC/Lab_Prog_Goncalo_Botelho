import random
from datetime import datetime

def calcular_paridade_par(n):
    """Calcula o bit de paridade par."""

    return bin(n).count('1') % 2

def alterar_um_bit(n):
    """Inverte um bit aleatório num número de 7 bits (0-127)."""

    posicao = random.randint(0, 6)
    return n ^ (1 << posicao)

def main():

    random.seed(datetime.now().timestamp())

    k = random.randint(51, 64)
    
    dados_processados = []
    lista_erros_detetados = []
    
    numeros_originais = [random.randint(0, 127) for _ in range(k)]
    indices_para_erro = random.sample(range(k), k // 5)

    for i in range(k):
        n_orig = numeros_originais[i]
        p1 = calcular_paridade_par(n_orig)
        
        if i in indices_para_erro:
            n_recebido = alterar_um_bit(n_orig)
        else:
            n_recebido = n_orig
            
        p2 = calcular_paridade_par(n_recebido)
        teve_erro = (p1 != p2)
        
        if teve_erro:
            lista_erros_detetados.append(i + 1) 
            
        dados_processados.append({
            'num': n_orig,
            'p1': p1,
            'p2': p2,
            'status': "INVÁLIDO" if teve_erro else "OK"
        })
    
    if lista_erros_detetados:
        print(f"ERROS DETETADOS nos índices: {lista_erros_detetados}")
        print(f"Total de falhas: {len(lista_erros_detetados)}")
    else:
        print("Nenhum erro detetado.")

    nome_ficheiro = "relatorio_final.txt"

    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write(f"Total de registos: {k}\n\n")
        f.write(f"{'Índice':^8} | {'Número':^8} | {'Paridade 1':^12} | {'Paridade 2':^12} | {'Status':^8}\n")
        
        for idx, item in enumerate(dados_processados):
            f.write(f"{idx+1:^8} | {item['num']:^8} | {item['p1']:^12} | {item['p2']:^12} | {item['status']:^8}\n")
        
        if lista_erros_detetados:
            f.write(f"\nRESUMO: Foram encontrados erros nos índices: {lista_erros_detetados}\n")
        else:
            f.write("\nRESUMO: Todos os bits de paridade estão corretos.\n")

    print(f"\nSucesso! O ficheiro '{nome_ficheiro}' foi gerado com os detalhes.")

if __name__ == "__main__":
    main()