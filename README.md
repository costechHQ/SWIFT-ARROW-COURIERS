# Swift Arrow Couriers

## About

Swift Arrow Couriers is a Python terminal-based parcel tracking system. It allows staff to log in and perform operations such as finding, creating, updating and deleting parcels.

The parcel data is stored in `parcels.json`, which contains about 50,000 parcels.

## Project Structure

```text
swift-arrow-couriers/
│
├── main.py
├── parcels.json
├── README.txt
│
└── courier/
    ├── auth.py
    ├── cache.py
    ├── index.py
    ├── parser.py
    ├── services.py
    ├── staff.py
    ├── storage.py
    └── ultils.py
```

I separated the project into modules so that each part of the program has a specific job.

## Index

I created one index with two lookup sections:

```python
{
    "by_tracking_code": {},
    "by_destination": {}
}
```

The tracking code index stores the position of a parcel in the list. This means the program doesn't have to search through all 50,000 parcels to find one parcel.

The destination index stores the positions of parcels going to each city.

## Cache

The cache stores the 10 most recent search results.

If the same request is made again, the program can return the previous result from the cache instead of doing the search again.

When a parcel is updated, its cached result is removed so that an old result is not returned.

## Authentication

Staff members sign in with a username and password.

Passwords are stored as SHA-256 hashes instead of readable passwords.

After login, the program creates a random token that acts as the staff member's day pass. The token is used for later requests instead of entering the password again.

The token expires after five minutes and signing out removes it.

## Permissions

There are two main positions:

* Station Master
* Clerk

Only the Station Master can delete parcels. If a Clerk tries to delete one, the program returns `403`.

## Parcel Operations

The program supports:

```text
GET parcel <tracking_code>
GET parcels to <city>
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

This project helped me understand how indexing can make searching faster, how caching avoids repeating work, and why cached data needs to be invalidated when the original data changes.

I also learned the difference between password hashing, authentication with tokens, and authorization based on a user's position.

## Running the Project

```bash
uv run main.py
```

The program opens the tracking window and asks the staff member to sign in before accepting requests.
