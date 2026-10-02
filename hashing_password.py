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

# print(hashing_password("daston8747"))
#
# print(verify_password(password="dastons8747",
#                       hashed_password="$argon2id$v=19$m=65536,t=3,p=4$kRxafkfFVM9ntEcvD47LiQ$0lUbTtwOd+SUapHQwFPSRrJu0kuszhthIjK/zjXWRMY"))
# print(generate_session_id())
