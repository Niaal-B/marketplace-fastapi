from fastapi import FastAPI,HTTPException
from auth import hash_password,verify_password,create_access_token
from database import users_collection
from models import UserCreate
from datetime import timedelta


app = FastAPI()

@app.post("/signup")
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one({"email" : user.email})
    if existing_user:
        raise HTTPException(status_code=400,detail="Email Already Registred")

    hashed_password = hash_password(user.password)
    new_user = {"email" : user.email , "hashed_password" : hashed_password}
    await users_collection.insert_one(new_user)

    return {"message" : "User created successfully"}


@app.post("/login")
async def login(user: UserCreate):
    db_user = await users_collection.find_one({"email":user.email})

    if not db_user or not verify_password(user.password,db_user["hashed_password"]):
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/listusers")
async def user_list():
    user_cursor =  users_collection.find({},{"_id":0})
    all_users = await user_cursor.to_list(length=None)
    return {"users" : all_users}