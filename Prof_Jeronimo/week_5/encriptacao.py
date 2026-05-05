def encriptar(texto, chave):
    """Encripta um texto deslocando o valor ASCII de cada carácter."""
    resultado = ""
    if isinstance(chave, int):
        chave = [chave]
    for i, char in enumerate(texto):
        valorascii = ord(char)
        k = chave[i % len(chave)]
        novovalor = (valorascii + k) % 128
        resultado += chr(novovalor)
    return resultado

def desencriptar(texto, chave):
    """Desencripta um texto subtraindo a chave ao valor ASCII."""
    resultado = ""
    if isinstance(chave, int):
        chave = [chave]
    for i, char in enumerate(texto):
        valorascii = ord(char)
        k = chave[i % len(chave)]
        novovalor = (valorascii - k) % 128
        resultado += chr(novovalor)
    return resultado

def encriptar_ficheiro(entrada, saida, chave):
    """Lê um ficheiro de texto, encripta o conteúdo e guarda num novo ficheiro."""
    with open(entrada, "r") as f:
        texto = f.read()
    texto_encriptado = encriptar(texto, chave)
    with open(saida, "w") as f:
        f.write(texto_encriptado)

def desencriptar_ficheiro(entrada, saida, chave):
    """Desencripta um ficheiro previamente encriptado."""
    with open(entrada, "r") as f:
        texto = f.read()
    texto_desencriptado = desencriptar(texto, chave)
    with open(saida, "w") as f:
        f.write(texto_desencriptado)

def encriptar_campo(ficheiro_entrada, ficheiro_saida, chave, indice_campo):
    """Encripta apenas um campo específico de cada linha de um ficheiro onde os campos são separados por ';'."""
    with open(ficheiro_entrada, "r") as f:
        linhas = f.readlines()
    with open(ficheiro_saida, "w") as f:
        for linha in linhas:
            campos = linha.strip().split(";")
            if indice_campo < len(campos):
                campos[indice_campo] = encriptar(campos[indice_campo], chave)
            nova_linha = ";".join(campos)
            f.write(nova_linha + "\n")

def salvar_txt(textoencriptado, textodesencriptado):
    with open("mensagem_encriptada.txt", "w") as f:
        f.write("Texto encriptado: " + textoencriptado + "\n")
        f.write("Texto desencriptado: " + textodesencriptado + "\n")

def main():
    textoincriptar = input("Escreva uma mensagem para encriptar: ")
    chave = []
    numerochaves = input("Deseja utilizar multiplas chaves? (y/n): ").lower()
    if numerochaves == "n":
        chaveinput = int(input("Digite a chave: "))
        chave.append(chaveinput)
    elif numerochaves == "y":
        for i in range(len(textoincriptar)//2):
            chaveinput = int(input(f"Digite a chave {i+1}: "))
            chave.append(chaveinput)

    textoencriptado = encriptar(textoincriptar, chave)
    textodesencriptado = desencriptar(textoencriptado, chave)
    salvar_txt(textoencriptado, textodesencriptado)

    print("Texto original:", textoincriptar)
    print("Encriptado:", textoencriptado)
    print("Desencriptado:", textodesencriptado)
    if textoincriptar == textodesencriptado:
        print("Verificação: OK")
    else:
        print("Erro na desencriptação")

if __name__ == "__main__":  main()