def hash_folding_final(texto, n=5):

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
    
    blocos, h_base = hash_folding_final(texto, n)
    
    assinatura = []
    for i in range(n):
        valor_hash = int(h_base[i], 16)
        valor_chave = chave_lista[i % len(chave_lista)]
        
        soma_assinatura = (valor_hash + valor_chave) % 256
        assinatura.append(f"{soma_assinatura:02X}")
        
    return blocos, h_base, assinatura

def main():
    mensagem =str(input("Insira uma mensagem: "))
    chave_secreta = [10, 20, 30]

    b, h, s = keyed_hash_final(mensagem, chave_secreta, n=5)

    print(f"Blocos ASCII: {b}")
    print(f"Hash (Integridade): {h}")
    print(f"Assinatura (Autenticidade): {s}")

if __name__ == "__main__":
    main()