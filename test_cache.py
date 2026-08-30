from courier.cache import Cache

cache = Cache(3)

cache.set("A", "Apple")
cache.set("B", "Banana")
cache.set("C", "Cherry")

print(cache.data)

cache.set("D", "Date")

print(cache.data)

print(cache.get("C"))

print(cache.data)