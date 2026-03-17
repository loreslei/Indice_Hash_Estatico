from paginas_hash import Bucket, HashTable, Page, table_scan
import time

# O índice hash a ser implementado é dinâmico, não estático

tuples_per_page = int(input("Digite uma quantidade de tuplas por página: "))

pages = []
page_number = 0


with open("words.txt", "r") as f:
    tuples = f.read().splitlines()


pages = Page.paginate(tuples, tuples_per_page)

print("Total de registros:", len(tuples))
print("Total de páginas:", len(pages))

print("\nPrimeira e Última Páginas:")
if pages:
    example_page = pages[0]
    print(f"Número da página: {example_page.number}")
    print(f"Registros na página: {len(example_page.records)}")
    print("Primeiros registros:", example_page.records[:5])
    
    example_page = pages[len(pages)-1]
    print(f"Número da página: {example_page.number}")
    print(f"Registros na página: {len(example_page.records)}")
    print("Primeiros registros:", example_page.records[:5])
    
    
bucket_capacity = 10
    
hash_table = HashTable(bucket_capacity)

for page in pages:
    for key in page.records:
        hash_table.insert_hash(key, page.number)

hash_table.print_statistics()
word = input("Digite a chave a ser pesquisada: ")
#hash_table.print_hash()
print(hash_table.search(word))
print(table_scan(pages, word))

