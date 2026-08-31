from courier.cache import Cache

cache = Cache(10)

cities = [
    "Kano",
    "Aba",
    "Lagos",
    "Abuja",
    "Enugu",
    "Ibadan",
    "Jos",
    "Uyo",
    "Calabar",
    "Onitsha"
]

for city in cities:
    cache.set(f"destination:{city}", city)

print("After 10 entries:")
print(cache.data)

cache.set("destination:Owerri", "Owerri")

print("\nAfter 11th entry:")
print(cache.data)

print("\nKano:")
print(cache.get("destination:Kano"))

print("\nOwerri:")
print(cache.get("destination:Owerri"))