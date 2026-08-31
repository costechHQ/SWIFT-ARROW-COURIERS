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
            f"There is no parcel {tracking_code}. "
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
    """Formats a raw parcel dictionary into a human readable text block."""

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
    """Validates and appends a new parcel to the tracking ledger."""

    tracking_code = parcel_data.get("tracking_code")

    if not tracking_code:
        return 400, "Tracking code is required."

    if tracking_code in tracking_index["by_tracking_code"]:
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

    tracking_index["by_tracking_code"][tracking_code] = position

    destination = parcel_data["destination"]
    if destination not in tracking_index["by_destination"]:
        tracking_index["by_destination"][destination] = []

    tracking_index["by_destination"][destination].append(position)

    parcel_status = parcel_data["status"]
    if parcel_status not in tracking_index["by_status"]:
        tracking_index["by_status"][parcel_status] = []

    tracking_index["by_status"][parcel_status].append(position)

    return 201, parcel_data


def update_parcel(tracking_code, new_status, parcels, track_index, cache):
    position = track_index["by_tracking_code"].get(tracking_code)

    if position is None:
        return 404, f"There is no parcel {tracking_code}."

    parcel = parcels[position]

    if parcel is None:
        return 404, f"There is no parcel {tracking_code}."

    old_status = parcel["status"]

    if old_status in track_index["by_status"]:
        if position in track_index["by_status"][old_status]:
            track_index["by_status"][old_status].remove(position)

    if new_status not in track_index["by_status"]:
        track_index["by_status"][new_status] = []

    track_index["by_status"][new_status].append(position)

    parcel["status"] = new_status

    cache.delete(tracking_code)
    cache.delete(f"status:{old_status}")
    cache.delete(f"status:{new_status}")

    return 200, parcel


def get_parcel_by_destination(destination, parcels, index, cache):

    cache_key = f"destination:{destination}"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return (
            200,
            cached_result["results"],
            cached_result["milliseconds"],
            True
        )

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


def get_parcels_by_status(status, parcels, index, cache):

    cache_key = f"status:{status}"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return (
            200,
            cached_result["results"],
            cached_result["milliseconds"],
            True
        )

    start_time = time.perf_counter()

    positions = index["by_status"].get(status)

    if positions is None:
        elapsed = (time.perf_counter() - start_time) * 1000

        return (
            404,
            f"There are no parcels with status {status}.",
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