import json
import os
import hashlib

PARCELS_FILE = "parcels.json"
SEAL_FILE = "ledger_seal.txt"


def create_hash():
    with open(PARCELS_FILE, "r") as file:
        content = file.read()

    return hashlib.sha256(content.encode()).hexdigest()

#print(create_hash())




def load_parcels():
    """This function loads ledger"""
    if not os.path.exists(PARCELS_FILE):
        print("Ledger not found. Starting with an empty ledger.")
        return []
    try:
        with open(PARCELS_FILE, "r") as file:
            parcels = json.load(file)

            if not isinstance(parcels, list):
                print("Ledger format is invalid. Starting with an empty ledger.")
                return []
            return parcels

    except json.JSONDecodeError:
        print("Ledger could not be read. Starting with an empty ledger.")
        return []


def save_parcels(parcels):
    with open(PARCELS_FILE, "w") as file:
        json.dump(parcels, file, indent=2)
