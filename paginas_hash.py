class Page:
    def __init__(self, number):
        self.number = number
        self.records = []

class Bucket:
    def __init__(self, fr):
        self.capacity = fr
        self.data = []
        self.overflow = []