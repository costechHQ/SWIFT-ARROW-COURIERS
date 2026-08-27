from courier.storage import load_parcels
from courier.index import build_index
from courier.services import get_parcel, format_parcel_result
from courier.staff import load_staff
from courier.auth import login, validate_token, logout
from courier.parser import parse_slip

def main():
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


    print("=" * 55)
    print("           SWIFT ARROW COURIES")
    print("               TRACKING WINDOW")
    print("=" * 55)

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

# print(parse_slip("GET parcel SA-1998550-IY"))
# print(parse_slip("DANCE parcel SA-1998550-IY"))
            
            request = parse_slip(slip)

            if request is None:
                print(
                    "400 - I cannot read this slip. "
                    "The verbs are GET, POST, PUT, DELETE."
                )
                continue

            if (
                request["verb"] == "GET"
                and request["resource"] == "parcel"
            ):
                status, result = get_parcel(
                    request["tracking_code"],
                    parcels,
                    tracking_index
                )

                if status == 404:
                    print(f"{status} - {result}")
                else:
                    print(
                        f"{status} - Found in "
                        f"{result['millseconds']:.3f} ms"
                    )
                    print(format_parcel_result(result))

if __name__ == "__main__":
    main()