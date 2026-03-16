class HashTable:  
    def __init__(self, fr):
        self.capacity = fr  
        self.data = {}      
        self.buckets = {}   
        self.next_bucket = 0
        
    def hash_index(self, key):
        h = 0
        for char in key:
            h = h+1
            # h = (h * 31 + ord(char)) % (2**32) 
        return h
        
    def insert_hash(self, key, page_number):
        index = self.hash_index(key)
        
        if index not in self.data:
            address = self.next_bucket
            self.data[index] = [address]  
            self.buckets[address] = Bucket(self.capacity)
            self.next_bucket += 1
            
        
        addresses = self.data[index]
        current_address = addresses[-1]
        bucket = self.buckets[current_address]
        
        
        # if len(self.buckets[current_address]) >= self.capacity:
        if bucket.is_full():
            
            new_address = self.next_bucket
            addresses.append(new_address)
            self.buckets[new_address] = Bucket(self.capacity)
            self.next_bucket += 1
            current_address = new_address
            bucket = self.buckets[current_address]
            
        bucket.insert(key, page_number)
        # self.buckets[current_address].append((key, page_number))
    
    def search(self, key):
        index = self.hash_index(key)

        if index not in self.data:
            print("Chave não encontrada")
            return None

        addresses = self.data[index]

        for addr in addresses:
            bucket = self.buckets[addr]

            for k, page in bucket.records:
                if k == key:
                    print(f"\nChave encontrada!")
                    print(f"Bucket: {addr}")
                    print(f"Página: {page}")

                    print("\nConteúdo do Bucket:")
                    for record in bucket.records:
                        print(record)

                    return addr, page

        print("Chave não encontrada")
        return None
    
    def print_hash(self):
        print("\n--- ESTRUTURA DO ÍNDICE HASH ---")
        for index, addresses in self.data.items():
            print(f"Índice {index} aponta para os Buckets: {addresses}")
            for addr in addresses:
                bucket = self.buckets[addr]
                print(f"  Bucket {addr} (Registros: {len(bucket.records)}/{bucket.capacity}):")
                # for key, page in bucket.records:
                #     print(f"    -> Chave: '{key}', Página: {page}")
        
class Bucket:
    def __init__(self, capacity):
        self.capacity = capacity
        self.records = []
        
    def insert(self, key, page):
        if self.is_full():
            raise Exception("Bucket cheio")
        self.records.append((key, page))
        
    def is_full(self):
        return len(self.records) >= self.capacity
    
class Page:
    def __init__(self, number, records):
        self.number = number
        self.records = records
            
    @classmethod
    def paginate(cls, words, tuples_per_page):
        pages = []
        page_number = 1

        for i in range(0, len(words), tuples_per_page):
            records = words[i:i + tuples_per_page]
            
            page = cls(page_number, records)
            pages.append(page)

            page_number += 1

        return pages