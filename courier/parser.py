def parse_slip(slip):
    parts = slip.strip().split()

    if len(parts) == 0:
        return None

    verb = parts[0].upper()

    if verb not in {"GET", "POST", "PUT", "DELETE"}:
        return None

    if len(parts) < 2:
        return None

    resource = parts[1].lower()

    if resource == "parcel":
        if len(parts) != 3:
            return None

        return {
            "verb": verb,
            "resource": resource,
            "tracking_code": parts[2]
        }

    if resource == "parcels":
        if len(parts) != 4 or parts[2].lower() != "to":
            return None

        return {
            "verb": verb,
            "resource": resource,
            "destination": " ".join(parts[3:])
        }

    return None
