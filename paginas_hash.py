class Page:
    def __init__(self, number, records):
        self.number = number
        self.records = records

class Bucket:
    def __init__(self, fr):
        self.capacity = fr
        self.data = {}
        self.buckets = {}
        self.next_bucket = 0
        
    def hash_index(self, tuple):
        h = 0
        for char in tuple:
            # h = (h * 31 + ord(char)) % (2**32)
            h = h+1
        return h
        
    def insert_hash(self, tuple):
        index = self.hash_index(tuple)
        if index not in self.data:
            address = self.next_bucket
            self.data[index] = address
            self.buckets[address] = []
            self.next_bucket += 1
        else:
            address = self.data[index]
            
        self.buckets[address].append(tuple)
    
    def search(self, tuple):
        index = self.hash_index(tuple)
        
        if index not in self.data:
            return
        
        address = self.data[index]
        
        for word in self.buckets[address]:
            if word == tuple:
                return word
        return 
    
    def print_hash(self):

        print("\nÍNDICE HASH (index -> bucket)")
        for index, address in self.data.items():
            print(f"{index} -> Bucket {address}")

        print("\nBUCKETS (dados dentro)")
        for address, values in self.buckets.items():
            print(f"Bucket {address}:")
            for v in values:
                print("   ", v)
    
    

def paginate(words, tuples_per_page):

    pages = []
    page_number = 1

    for i in range(0, len(words), tuples_per_page):

        records = words[i:i + tuples_per_page]

        page = Page(page_number, records)
        pages.append(page)

        page_number += 1

    return pages




