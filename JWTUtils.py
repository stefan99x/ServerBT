import datetime

import jwt


class JWTUtils:
    def __init__(self) -> None:
        with open("JWTSecret.txt", "r") as secretFile:
            self.__secret = secretFile.readline().strip("\n")

    def encode_token(self, id, email):
        return jwt.encode(self.get_jwt_payload(id, email), self.__secret)

    def decode_token(self, token):
        return jwt.decode(token, self.__secret, algorithms=["HS256"])

    def get_jwt_payload(self, id, email):
        return {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=5),
            "iat": datetime.datetime.utcnow(),
            "id": str(id),
            "email": email,
        }
