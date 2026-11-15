from argon2 import PasswordHasher
from uuid import uuid4

hasher = PasswordHasher()


def generate_session_id():
    return str(uuid4())


def hashing_password(password):
    return hasher.hash(password)


def verify_password(password, hashed_password):
    try:
        return bool(hasher.verify(hashed_password, password))
    except:
        return False

#
# Misol (haqiqiy qiymatlarni .env faylida saqlang, kodga yozmang):
#
# secret_key = os.environ.get("SECRET_KEY")
# token = jwt.encode(key=secret_key, payload={"user_id": 1}, algorithm="HS256")
# print(token)
# print(decode)
