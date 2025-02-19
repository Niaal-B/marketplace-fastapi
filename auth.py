from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timezone






SECRET_KEY = "a3f2c9e8d76b4c5a1123456789abcdef1234567890abcdef1234567890abcdef"  # Replace with your generated key

ALOGRITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password) -> bool:
    return pwd_context.verify(plain_password,hashed_password)



def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Generates a JWT token with expiration """
    to_encode = data.copy() 
    
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALOGRITHM)
