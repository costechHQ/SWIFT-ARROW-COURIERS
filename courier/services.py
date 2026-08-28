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

def create_parcel(parcel_data, parcels, tracking_index):
    tracking_code = parcel_data.get("tracking_code")

    if not tracking_code:
        return 400, "Tracking code is required."

    if tracking_code in tracking_index:
        return 400, f"Parcel {tracking_code} already exist."

    required_fields = [
        "sender",
        "reciever",
        "origin",
        "destination",
        "status",
        "weight_kg",
        "date_shipped"
    ]

    for field in required_fields:
        if field not in parcel_data:
            return 400, f"Missing field: {field}"

    position = len(parcels)

    parcels.append(parcel_data)

    tracking_index[tracking_code] = position

    return 201, parcel_data