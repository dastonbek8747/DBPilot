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
# secret_key = os.environ.get('SECRET_KEY')
# # print(secret_key)
# # print(type(secret_key))
# payload = {"user_id": 1}
# token = jwt.encode(
#     key=secret_key,
#     payload=payload,
#     algorithm="HS256"
# )
# print(token)
#
# decode = jwt.decode(
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.RsjmMzDHuGR8Eu9Urrwp0tcL-qneQ3gDGQj9IenVZg0",
#     key=secret_key,
#     algorithms=["HS256"]
# )
# print(decode)
# print(hashing_password("daston8747"))
#
# print(verify_password(password="dastons8747",
#                       hashed_password="$argon2id$v=19$m=65536,t=3,p=4$kRxafkfFVM9ntEcvD47LiQ$0lUbTtwOd+SUapHQwFPSRrJu0kuszhthIjK/zjXWRMY"))
# print(generate_session_id())
