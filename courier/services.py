import time

def get_parcel(tracking_code, parcels, tracking_index, cache):
    cached_result = cache.get(tracking_code)

    if cached_result is not None:
        return 200, cached_result, True

    start_time = time.perf_counter()

    position = tracking_index["by_tracking_code"].get(tracking_code)

    if position is None:
        elapsed = (time.perf_counter() - start_time) * 1000

        return (
            404, 
            f"There is no parcel {tracking_code}." 
            f"Search took {elapsed:.3f} ms",
            False
        )

    parcel = parcels[position]

    elapsed = (time.perf_counter() - start_time) * 1000

    result = {
        "parcel": parcel,
        "milliseconds": elapsed
    }

    cache.set(tracking_code, result)

    return 200, result, False

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
    """validates and appends a new parcel to the tracking ledger
    """
    tracking_code = parcel_data.get("tracking_code")

    if not tracking_code:
        return 400, "Tracking code is required."

    if tracking_code in tracking_index:
        return 400, f"Parcel {tracking_code} already exist."

    required_fields = [
        "sender",
        "receiver",
        "origin",
        "destination",
        "status",
        "weight_kg",
        "date_shipped"
    ]

    for field in required_fields:
        if field not in parcel_data:
            return 400, f"Missing field: {field}"

    # position = len(parcels)

    # parcels.append(parcel_data)

    position = None

    for i, parcel in enumerate(parcels):
        if parcel is None:
            position = i
            break

    if position is None:
        position = len(parcels)
        parcels.append(parcel_data)
    else:
        parcels[position] = parcel_data

    tracking_index[tracking_code] = position

    return 201, parcel_data


def update_parcel(tracking_code, new_status, parcels, track_index, cache):

    position = track_index["by_tracking_code"].get(tracking_code)

    if position is None:
        return 404, f"There is no parcel {tracking_code}."

    parcel = parcels[position]

    if parcel is None:
        return 404, f"There is no parcel {tracking_code}."

    parcel["status"] = new_status

    cache.delete(tracking_code)

    return 200, parcel

def get_parcel_by_destination(destination, parcels, index, cache):

    cache_key = f"destination:{destination}"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return 200, cached_result["results"], cached_result["milliseconds"], True

    start_time = time.perf_counter()

    positions = index["by_destination"].get(destination)

    if positions is None:
        elapsed = (time.perf_counter() - start_time) * 1000

        return (
            404,
            f"There are no parcels heading to {destination}.",
            elapsed,
            False
        )
    
    results = []

    for position in positions:
        results.append(parcels[position])

    elapsed = (time.perf_counter() - start_time) * 1000

    cache.set(
        cache_key,
        {
            "results": results,
            "milliseconds": elapsed
        }
    )

    return 200, results, elapsed, False