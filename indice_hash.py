from paginas_hash import Bucket, Page

PAGE_SIZE = 8 * 1024  

tuples_per_page = 1000

pages = []
page_number = 0
current_page = Page(page_number)

with open("words.txt", "r") as f:
    words_data = f.read().splitlines()

words_count = len(words_data) 
print(words_count)


def paginate(words, tuples_per_page):

    pages = []
    page_number = 0

    for i in range(0, len(words), tuples_per_page):

        records = words[i:i + tuples_per_page]

        page = Page(page_number, records)
        pages.append(page)

        page_number += 1

    return pages