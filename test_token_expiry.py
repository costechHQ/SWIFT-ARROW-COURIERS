import time

from courier.auth import (
    generate_token,
    validate_token,
    active_tokens
)

token = generate_token()

active_tokens[token] = {
    "username": "test_user",
    "position": "Clerk",
    "issued_at": time.time()
}

print("Before expiry:")
print(validate_token(token))

active_tokens[token]["issued_at"] = time.time() - 301

print("\nAfter expiry:")
print(validate_token(token))

print("\nToken still exists:")
print(token in active_tokens)