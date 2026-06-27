from dacoolstore.security import hash_password, verify_password


def test_hash_password():
    password = "secret_password"
    hashed = hash_password(password)
    assert hashed != password
    assert hashed.startswith("pbkdf2_sha256$")


def test_verify_password_correct():
    password = "my_password"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    password = "my_password"
    hashed = hash_password(password)
    assert verify_password("wrong_password", hashed) is False


def test_verify_password_legacy():
    # Test fallback to plain text passwords
    plain_password = "legacy_plain_text"
    assert verify_password(plain_password, plain_password) is True
    assert verify_password("different", plain_password) is False


def test_verify_password_empty():
    assert verify_password("", "") is False
    assert verify_password("a", "") is False
    assert verify_password("", "a") is False
