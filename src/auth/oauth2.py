from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from src.database.crud import CRUD
from src.model.user import User
from typing import List

def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context().verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context().hash(password)

def get_users(crud: CRUD) -> List[User]:
    return crud.search(User, "disabled", False)

def authenticate_user(crud: CRUD, mail: str, password: str):
    users = get_users(crud)
    for user in users:
        if user.mail == mail and verify_password(password, user.password):
            return user
    return False

def create_access_token(data: dict, API):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=API['oauth2']['timeout'])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API['oauth2']['secret_key'], algorithm=API['oauth2']['algorithm'])
    return encoded_jwt