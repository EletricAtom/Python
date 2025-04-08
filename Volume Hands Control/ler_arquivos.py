import os

arquivos = os.listdir("musicas")
contador = 0
if contador > len(arquivos):
    contador = 0 
print(arquivos[contador])