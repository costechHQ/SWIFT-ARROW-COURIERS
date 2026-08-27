from courier.storage import load_parcels
from courier.index import build_index
from courier.services import get_parcel
from courier.staff import load_staff
from courier.auth import login, validate_token, logout


parcels = load_parcels()
tracking_index = build_index(parcels)
staff = load_staff()

# print("Parcels loaded:", len(parcels))
# print("Index enteries:", len(tracking_index))

# print(tracking_index["SA-1998500-IY"])

# code = "SA-1998500-IY"

# status, result = get_parcel(
#     code,
#     parcels,
#     tracking_index
# )

# print(status)
# print(result)

print("SWIFT ARROW COURIES")
print("---------------------")

username = input("Username: ")
password = input("Password: ")

token = login(username, password, staff)

if token is None:
    print("401 - Invalid username or password.")
else:
    session = validate_token(token)

    print(
        f"200 - Welcome, {session['username']} "
        f"({session['position']})."
    )

    print("Your day pass:", token)

    while True:
        slip = input("\nPass slip: ")

        if slip.upper() == "SIGN OUT":
            logout(token)
            print("200 - signed out successfully.")
            break

        session = validate_token(token)

        if session is None:
            print("401 - Invalid or expired day pass.")
            break

        print("Slip received:", slip)