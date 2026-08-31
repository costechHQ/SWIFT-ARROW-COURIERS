def build_index(parcels):
    """This function creates an index 
    memory map to optimize search performance"""

    index = {
        "by_tracking_code": {},
        "by_destination": {}
    }

    for position, parcel in enumerate(parcels):
        tracking_code = parcel["tracking_code"]
        destination = parcel["destination"]

        index["by_tracking_code"][tracking_code] = position

        if destination not in index["by_destination"]:
            index["by_destination"][destination] = []

        index["by_destination"][destination].append(position)

    return index