from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error

app = FastAPI()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Nanthakumar13@",
    "database": "ilaktech"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class UserCreate(BaseModel):
    name: str
    email: str
    phone_no: int
    subject: str
    message: str
    
@app.get("/users", response_model=list[UserCreate])
def read_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, email, phone_no, subject, message FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users
    
@app.post("/users", response_model=dict)
def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    print(user)
    query = "INSERT INTO users (name, email, phone_no, subject, message) VALUES (%s, %s, %d, %s, %s)"
    cursor.execute(query, (user.name, user.email, int(user.phone_no), user.subject, user.message))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "User created successfully"}