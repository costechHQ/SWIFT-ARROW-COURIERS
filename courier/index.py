def build_index(parcels):
    index = {}

    for position, parcel in enumerate(parcels):
        tracking_code = parcel["tracking_code"]
        index[tracking_code] = position

    return index