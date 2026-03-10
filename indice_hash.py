from paginas_hash import Bucket, Page, paginate

PAGE_SIZE = 8 * 1024  

tuples_per_page = 1000

pages = []
page_number = 0

#O índice hash a ser implementado é dinâmico, não estático no trabalho do Rafael


with open("words.txt", "r") as f:
    tuples = f.read().splitlines()

pages = paginate(tuples, tuples_per_page)

print("Total de registros:", len(tuples))
print("Total de páginas:", len(pages))

print("\nExemplo de página:")
if pages:
    example_page = pages[1]
    print(f"Número da página: {example_page.number}")
    print(f"Registros na página: {len(example_page.records)}")
    print("Primeiros registros:", example_page.records[:5])

