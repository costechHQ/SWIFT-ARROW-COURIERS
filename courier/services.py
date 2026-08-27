import time

def get_parcel(tracking_code, parcels, tracking_index):
    start_time = time.perf_counter()

    position = tracking_index.get(tracking_code)

    if position is None:
        elapsed = (time.perf_counter() - start_time) * 1000
        return 404, f"Parcel {tracking_code} not found. Search took {elapsed:.3f} ms"

    parcel = parcels[position]

    elapsed = (time.perf_counter() - start_time) * 1000

    return 200, {
        "parcel": parcel,
        "milliseconds": elapsed
    }