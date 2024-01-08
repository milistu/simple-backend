import os
import json
import bcrypt
from jose import jwt
from datetime import datetime, timedelta


def load_user_db(db_path: str = "./user_db.json") -> dict:
    with open(db_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt


if __name__ == "__main__":
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())

    database = load_user_db()
    print(database)

    plain_password = "ThisPasswordIsTheBest,TrustMe!"
    hashed_password = database["johndoe"]["hashed_password"]
    print(
        f"Passwords are the same: {verify_password(plain_password=plain_password, hashed_password=hashed_password)}"
    )
