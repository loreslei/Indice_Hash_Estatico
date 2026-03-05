with open("words.txt", "r") as f:
    data = f.read().splitlines()

qtd_palavras = len(data) 
print(qtd_palavras)
             