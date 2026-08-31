def build_index(parcels):
    """This function creates an index 
    memory map to optimize search performance"""

    index = {
        "by_tracking_code": {},
        "by_destination": {},
        "by_status": {}
    }

    for position, parcel in enumerate(parcels):
        tracking_code = parcel["tracking_code"]
        destination = parcel["destination"]
        status = parcel["status"]

        index["by_tracking_code"][tracking_code] = position

        if destination not in index["by_destination"]:
            index["by_destination"][destination] = []

        index["by_destination"][destination].append(position)

        if status not in index["by_status"]:
            index["by_status"][status] = []

        index["by_status"][status].append(position)

    return index