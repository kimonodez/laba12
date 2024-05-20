from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

# Колекції в MongoDB
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]

# Модель користувача
class User(BaseModel):
    username: str
    email: str

# Модель поста
class Post(BaseModel):
    title: str
    content: str
    author: str

# Модель коментарія
class Comment(BaseModel):
    content: str
    author: str
    post_id: str

# Додати користувача
@app.post("/users/")
async def create_user(user: User):
    user_id = users_collection.insert_one(user.dict()).inserted_id
    return {"user_id": str(user_id)}

# Отримати користувача за ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": user_id})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Створити пост
@app.post("/posts/")
async def create_post(post: Post):
    post_id = posts_collection.insert_one(post.dict()).inserted_id
    return {"post_id": str(post_id)}

# Отримати пост за ID
@app.get("/posts/{post_id}")
async def get_post(post_id: str):
    post = posts_collection.find_one({"_id": post_id})
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Створити коментар
@app.post("/comments/")
async def create_comment(comment: Comment):
    comment_id = comments_collection.insert_one(comment.dict()).inserted_id
    return {"comment_id": str(comment_id)}

# Отримати коментар за ID
@app.get("/comments/{comment_id}")
async def get_comment(comment_id: str):
    comment = comments_collection.find_one({"_id": comment_id})
    if comment:
        return comment
    else:
        raise HTTPException(status_code=404, detail="Comment not found")
