from collections import OrderedDict

class Cache:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None

        value = self.data.pop(key)
        self.data[key] = value

        return value

    def set(self, key, value):
        if key in self.data:
            self.data.pop(key)

        self.data[key] = value

        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def delete(self, key):
        self.data.pop(key, None)

    def clear(self):
        self.data.clear()