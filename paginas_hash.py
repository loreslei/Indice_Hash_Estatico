class Page:
    def __init__(self, number, records):
        self.number = number
        self.records = records

class Bucket:
    def __init__(self, fr):
        self.capacity = fr
        self.data = []
        self.overflow = []
        

def paginate(words, tuples_per_page):
    

    pages = []
    page_number = 1

    for i in range(0, len(words), tuples_per_page):

        records = words[i:i + tuples_per_page]

        page = Page(page_number, records)
        pages.append(page)

        page_number += 1

    return pages