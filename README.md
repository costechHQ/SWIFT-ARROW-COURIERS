# Swift Arrow Couriers


[![wakatime](https://wakatime.com/badge/github/costechHQ/SWIFT-ARROW-COURIERS.svg)](https://wakatime.com/badge/github/costechHQ/SWIFT-ARROW-COURIERS)

## About

Swift Arrow Couriers is a Python terminal-based parcel tracking system. It allows staff to log in and perform operations such as finding, creating and updating parcels.

The parcel data is stored in `parcels.json`, which contains about 50,000 parcels.

## Project Structure

```text
swift-arrow-couriers/

── main.py
── parcels.json
── ledger_seal.txt
── README.txt

── courier/
    ── auth.py
    ── cache.py
    ── index.py
    ── parser.py
    ── services.py
    ── staff.py
    ── storage.py
    ── utils.py
```

I separated the project into modules so that each part of the program has a specific job.

## Index

I created one index with three lookup sections:

```python
{
    "by_tracking_code": {},
    "by_destination": {},
    "by_status": {}
}
```

The tracking code index stores the position of a parcel in the list. This avoids searching through all the parcels to find one parcel.

The destination index stores the positions of parcels going to each destination.

The status index stores the positions of parcels based on their status. This allows requests such as:

```text
GET parcels status delivered
```

to be handled using the index.

## Cache

The cache stores recent search results.

If the same request is made again, the program can return the previous result from the cache instead of doing the search again.

The cache is also cleared when relevant parcel data is updated so that an old result is not returned.

## Authentication

Staff members sign in with a username and password.

Passwords are stored as SHA-256 hashes instead of readable passwords.

After login, the program creates a random token that acts as the staff member's day pass.

The token is used for later requests instead of entering the password again.

The token expires after five minutes and signing out removes it.

## Permissions

There are two main positions:

* Station Master
* Clerk

Only the Station Master can delete parcels. If a Clerk tries to delete one, the program returns `403`.

## Ledger Integrity

I added a hash check for `parcels.json`.

When the ledger is sealed, a SHA-256 hash is saved in:

```text
ledger_seal.txt
```

When the program starts, it creates a new hash and compares it with the saved one.

If they are different, the program reports that the ledger may have been changed and stops.

## Parcel Operations

The program supports:

```text
GET parcel <tracking_code>
GET parcels to <destination>
GET parcels status <status>
POST parcel
PUT parcel <tracking_code>
DELETE parcel <tracking_code>
```

Changes made to parcels are saved back to `parcels.json`, so they remain after restarting the program.

## Status Codes

The program uses:

```text
200 - Successful request
201 - Created
400 - Bad request
401 - Invalid/expired authentication
403 - Permission denied
404 - Not found
```

## What I Learned

This project helped me understand how indexing can make searching faster and how caching avoids repeating the same work.

I also learned why cached data needs to be cleared when the original data changes.

The authentication part helped me understand password hashing, tokens and permissions.

I also learned how a file can be checked for unexpected changes using a hash.

## Running the Project

```bash
uv run main.py
```

The program opens the tracking window and asks the staff member to sign in before accepting requests.
