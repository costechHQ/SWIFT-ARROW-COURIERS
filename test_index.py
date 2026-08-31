from courier.storage import load_parcels
from courier.index import build_index

parcels = load_parcels()

index = build_index(parcels)

code = "SA-1998500-IY"

print("Parcel code:", parcels[0]["tracking_code"])

print("Index value:", index["by_tracking_code"].get(code))

print("Code exists:", code in index["by_tracking_code"])

print("Status index:", len(index["by_status"]))

print("Delivered:", len(index["by_status"]["delivered"]))