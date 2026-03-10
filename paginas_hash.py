class Page:
    def __init__(self, number, records):
        self.number = number
        self.records = records

class Bucket:
    def __init__(self, fr):
        self.capacity = fr
        self.data = []
        self.overflow = []
        
    def hash_index(tuple):
        h = 0
        for char in tuple:
            h = (h * 31 + ord(char)) % (2**32)
        return h
        
    def insert_hash(self, tuple, value):
        index = self.hash_index(tuple)
        self.data[index].append((tuple, value))
    
    def search(self, tuple):
        index = self.hash_index(tuple)
        
        for t, v in self.data[index]:
            if t == tuple:
                return v
        return 
    
    
        

def paginate(words, tuples_per_page):

    pages = []
    page_number = 1

    for i in range(0, len(words), tuples_per_page):

        records = words[i:i + tuples_per_page]

        page = Page(page_number, records)
        pages.append(page)

        page_number += 1

    return pages




