import time

lista = ['0','1','2','3','4','5','6','7','8','9']
key = input("Digite a senha: ")
base = len(lista)
tamanho = len(key)

# Começamos com todos os índices zerados
indices = [0] * tamanho

encontrado = False

start = time.time()
while not encontrado:
    # Gera a combinação atual com base nos índices
    tentativa = ''.join([lista[i] for i in indices])
    print("Tentando:", tentativa)

    if tentativa == key:
        print("Senha encontrada:", tentativa)
        encontrado = True
        break

    # Atualiza os índices como se fosse um número em base N
    for i in range(tamanho - 1, -1, -1):
        indices[i] += 1
        if indices[i] < base:
            break
        else:
            indices[i] = 0


end = time.time()
print(f"Tempo de execução: {end - start:.4f} segundos")