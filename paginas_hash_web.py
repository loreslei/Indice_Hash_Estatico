class HashTable:  
    def __init__(self, fr):
        self.capacity = fr  
        self.data = {}      
        self.buckets = {}   
        self.next_bucket = 0
        self.overflows = 0
        self.colisions = 0
        self.insertions = 0
        
    def hash_index(self, key):
        h = 0
        for char in key:
            #h = h + 1
            h = (h * 31 + ord(char)) % (2**32) 
        return h
        
    def insert_hash(self, key, page_number):
        # key = key.lower()
        
        self.insertions += 1
        
        index = self.hash_index(key)
        
        if index not in self.data:
            address = self.next_bucket
            self.data[index] = [address]  
            self.buckets[address] = Bucket(self.capacity)
            self.next_bucket += 1
        else:
            self.colisions += 1
            
        
        addresses = self.data[index]
        current_address = addresses[-1]
        bucket = self.buckets[current_address]
        
        
        # if len(self.buckets[current_address]) >= self.capacity:
        if bucket.is_full():
            self.overflows += 1
            
            new_address = self.next_bucket
            addresses.append(new_address)
            self.buckets[new_address] = Bucket(self.capacity)
            self.next_bucket += 1
            current_address = new_address
            bucket = self.buckets[current_address]
            
        bucket.insert(key, page_number)
        # self.buckets[current_address].append((key, page_number))
    
    
    def search(self, key):
        # key = key.lower()
        index = self.hash_index(key)

        if index not in self.data:
            return {"encontrado": False, "mensagem": "Chave não encontrada"}

        addresses = self.data[index]
        contador = 0

        for addr in addresses:
            bucket = self.buckets[addr]
            contador += 1

            for k, page in bucket.records:
                if k == key:
                    return {
                        "encontrado": True,
                        "bucket": addr,
                        "pagina": page,
                        "acessos_feitos": contador,
                        "conteudo_bucket": bucket.records
                    }

        return {"encontrado": False, "mensagem": "Chave não encontrada"}

    
    
    def get_statistics(self):
        colisions_percentage = (self.colisions / self.insertions) * 100 if self.insertions > 0 else 0
        return {
            "total_insercoes": self.insertions,
            "total_colisoes": self.colisions,
            "taxa_colisoes_pct": round(colisions_percentage, 2),
            "total_overflows": self.overflows
        }
    
    def get_hash_structure(self, incluir_registros=False):
        """
        Retorna a estrutura completa do índice Hash em formato de dicionário (JSON).
        Se incluir_registros for True, retorna também as chaves guardadas.
        """
        estrutura = []
        
        for index, addresses in self.data.items():
            indice_info = {
                "indice": index,
                "enderecos_buckets": addresses,
                "detalhes_buckets": []
            }
            
            for addr in addresses:
                bucket = self.buckets[addr]
                bucket_info = {
                    "id_bucket": addr,
                    "quantidade_registros": len(bucket.records),
                    "capacidade": bucket.capacity
                }
                
                # Se quiser ver os dados reais (a parte que estava comentada)
                if incluir_registros:
                    # Converte a tupla (key, page) em um dicionário para ficar bonito no JSON
                    bucket_info["registros"] = [{"chave": k, "pagina": p} for k, p in bucket.records]
                
                indice_info["detalhes_buckets"].append(bucket_info)
            
            estrutura.append(indice_info)
            
        return estrutura
        
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
    


def table_scan(pages, search_key):
    pages_accessed = 0
    # search_key = search_key.lower()
    
    for page in pages:
        pages_accessed += 1
        
        for key in page.records:
            if key == search_key:
                return {
                    "encontrado": True,
                    "pagina": page.number,
                    "custo_paginas_lidas": pages_accessed
                }
                
    return {
        "encontrado": False,
        "custo_paginas_lidas": pages_accessed,
        "mensagem": "Chave não encontrada (tabela inteira lida)"
    }