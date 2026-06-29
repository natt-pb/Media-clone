from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

# Database Connection Loop
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='Nostalgia007#',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error:", error)
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!"}

# 1. GET ALL POSTS (SQL)
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# 2. CREATE POST (SQL - Fixed attribute crash)
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
        (post.title, post.content, post.publish) # Fixed to post.publish
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# 3. GET SINGLE POST (SQL version to keep data synchronized)
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# 4. DELETE POST (SQL version with safety validation check)
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
                            
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING *""", 
        (post.title, post.content, post.publish, str(id),))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}


    
