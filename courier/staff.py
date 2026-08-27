import json
import os

from courier.auth import hash_password

STAFF_FILE = "staff.json"

INITIAL_STAFF = [
    {
        "username": "oga_musty",
        "password": "stationmaster1",
        "position": "Station Master"
    },
    {
        "username": "kemi_dispatch",
        "password": "parcels4kemi",
        "position": "Clerk"
    },
    {
        "username": "ibrahim_k",
        "password": "fastdelivery",
        "position": "Clerk"
    },
    {
        "username": "ngozi_front",
        "password": "desk2026",
        "position": "Clerk"
    }
]

def load_staff():
    if not os.path.exists(STAFF_FILE):
        staff = []

        for user in INITIAL_STAFF:
            staff.append({
                "username": user["username"],
                "password_hash": hash_password(user["password"]),
                "position": user["position"]
            })

        with open(STAFF_FILE, "w") as file:
            json.dump(staff, file, indent=2)

        return staff
    
    with open(STAFF_FILE, "r") as file:
        return json.load(file)
