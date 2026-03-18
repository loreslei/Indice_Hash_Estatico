from paginas_hash import Bucket, HashTable, Page, table_scan
import time


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
    
    
bucket_capacity = 100

hash_table = HashTable(bucket_capacity)

for page in pages:
    for key in page.records:
        hash_table.insert_hash(key, page.number)
        
print("\n" * 1)        
print("Estatísticas Gerais!!!!")
hash_table.print_statistics()

print("\n" * 1)
print("BUSCAS (0-0)")

word = input("Digite a chave a ser pesquisada: ")

print("BUSCA COM INDICE")

start_time_index = time.perf_counter()
    
print(hash_table.search(word))

end_time_index = time.perf_counter()

print("\n" * 1)


print("BUSCA COM TABLE SCAN")

start_time_table_scan = time.perf_counter() 

print(table_scan(pages, word))

end_time_table_scan = time.perf_counter()

print("\n" * 1)

time_spent_hash_index = round(end_time_index - start_time_index, 4)
time_spent_table_scan = round(end_time_table_scan - start_time_table_scan, 4)
speed_gain = 100 - ((time_spent_hash_index/time_spent_table_scan) * 100)
speedup = ((time_spent_table_scan - time_spent_hash_index)/time_spent_hash_index)

print("Comparação de tempo:")
print(f"Índice Hash: {time_spent_hash_index}")
print(f"Table Scan: {time_spent_table_scan}")
print(f"Redução de Tempo Índice Hash vs. Table Scan: {round(speed_gain, 2)}%")
print(f"Ganho de Tempo Índice Hash vs. Table Scan: {round(speedup, 2)}x")

