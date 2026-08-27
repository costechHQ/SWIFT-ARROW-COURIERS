def build_index(parcels):
    """This function creates an index 
    memory map to optimize search performance"""
    
    index = {}

    for position, parcel in enumerate(parcels):
        tracking_code = parcel["tracking_code"]
        index[tracking_code] = position

    return index