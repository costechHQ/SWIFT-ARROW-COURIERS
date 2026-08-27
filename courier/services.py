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

def format_parcel_result(result):
    """formats a raw parcel dictionary into a human readable text block"""
    parcel = result["parcel"]

    return (
        f"{parcel['tracking_code']} | "
        f"{parcel['sender']} -> {parcel['receiver']}\n"
        f"{parcel['origin']} -> {parcel['destination']} | "
        f"{parcel['status']} | "
        f"{parcel['weight_kg']} kg | "
        f"shipped {parcel['date_shipped']}"
    )