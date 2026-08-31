from courier.storage import load_parcels
from courier.index import build_index
from courier.services import (
    get_parcel,
    format_parcel_result,
    create_parcel,
    update_parcel,
    get_parcel_by_destination)
format_parcel_result, create_parcel
from courier.staff import load_staff
from courier.auth import login, validate_token, logout
from courier.parser import parse_slip
from courier.storage import load_parcels, save_parcels
from courier.ultils import read_float
from courier.cache import Cache




def main():
    parcels = load_parcels()
    tracking_index = build_index(parcels)
    staff = load_staff()
    cache = Cache(10)

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
                status, result, from_cache = get_parcel(
                    request["tracking_code"],
                    parcels,
                    tracking_index,
                    cache
                )

                if status == 404:
                    print(f"{status} - {result}")

                else: 
                    if from_cache:
                        print(
                            f"{status} - Found in "
                            f"{result['milliseconds']:3f} ms "
                            f"(from the tray)"
                        )
                    else:
                        print(
                        f"{status} - Found in "
                        f"{result['milliseconds']:.3f} ms"
                    )
                    print(format_parcel_result(result))

            elif (
                request["verb"] == "GET"
                and request["resource"] == "parcels"
            ):
                destination = request["destination"]

                status, result, milliseconds = get_parcel_by_destination(
                    destination,
                    parcels,
                    tracking_index
                )

                if status == 404:
                    print(f"{status} - {result}")
                else:
                    print(
                        f"{status} - {len(result)} parcel found "
                        f"in {milliseconds:.3f} ms."
                    )

                    for parcel in result:
                        print(
                            f"{parcel['tracking_code']} | "
                            f"{parcel['sender']} -> "
                            f"{parcel['receiver']} | "
                            f"{parcel['status']}"
                        )
                continue


            elif (
                    request["verb"] == "POST"
                    and request["resource"] == "parcel"
            ):
                print("\n--- NEW PARCEL ---")

                parcel_data = {
                        "tracking_code": input("Tracking code: ").strip(),
                        "sender": input("Sender: ").strip(),
                        "receiver": input("Receiver: ").strip(),
                        "origin": input("Origin: ").strip(),
                        "destination": input("Destination: ").strip(),
                        "status": input("Status: ").strip(),
                        "weight_kg": input("Weight (kg): ").strip(),
                        "date_shipped": input("Date_shipped: ").strip()
                }

                status, result = create_parcel(
                        parcel_data,
                        parcels,
                        tracking_index
                )

                if status == 201:
                    save_parcels(parcels)
                    print(f"201 - Parcel "
                              f"{parcel_data['tracking_code']} registered successfully.")
                else:
                    print(f"{status} - {result}")

                continue

            elif (
                request["verb"] == "PUT"
                and request["resource"] == "parcel"
            ):
                tracking_code = request["tracking_code"]

                print("\n--- UPDATE PARCEL ---")

                new_status = input("New status: ").strip()

                if not new_status:
                    print("400 - Status cannot be empty.")
                    continue

                status, result = update_parcel(
                    tracking_code,
                    new_status,
                    parcels,
                    tracking_index,
                    cache
                )

                if status == 200:
                    save_parcels(parcels)

                    print(
                        f"200 - Parcel {tracking_code}"
                        f"updated successfully."
                    )

                else:
                    print(f"{status} - {result}")

                continue

if __name__ == "__main__":
    main()