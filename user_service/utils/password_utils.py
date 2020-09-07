import bcrypt


def hash_password(raw_password: str) -> str:
    pass_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())
    return pass_hash.decode()


def is_password_valid(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())
