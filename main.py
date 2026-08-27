from courier.storage import load_parcels
from courier.index import build_index
from courier.services import get_parcel


parcels = load_parcels()
tracking_index = build_index(parcels)

# print("Parcels loaded:", len(parcels))
# print("Index enteries:", len(tracking_index))

# print(tracking_index["SA-1998500-IY"])

code = "SA-1998500-IY"

status, result = get_parcel(
    code,
    parcels,
    tracking_index
)

print(status)
print(result)