import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a random salt.

    Returns:
        A string formatted as pbkdf2_sha256$iterations$salt_hex$hash_hex
    """
    if not password:
        return ""
    salt = secrets.token_bytes(16)
    iterations = 100000
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${hashed.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a stored PBKDF2 hash.
    Supports fallback to plain-text check for legacy/existing records.
    """
    if not hashed_password or not password:
        return False

    # Check if the stored password is formatted as a PBKDF2 hash
    if not hashed_password.startswith("pbkdf2_sha256$"):
        # Legacy fallback
        return password == hashed_password

    try:
        parts = hashed_password.split("$")
        if len(parts) != 4:
            return False

        _, iterations_str, salt_hex, hash_hex = parts
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return secrets.compare_digest(actual_hash, expected_hash)
    except Exception:
        # If there's any parsing or decoding error, assume verification failed
        return False
