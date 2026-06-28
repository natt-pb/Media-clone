from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "I like Pizza", "id": 2}]
class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!"}

@app.get("/post")
def get_posts():
    return{"data": my_posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(1, 1000000)
    my_posts.append(post_dict)
    return{"data": post_dict}
#title str, content str



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(int(id))
    print(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id):
    index = find_index(id)

    my_posts.pop(index)
    return {"message": "post was successfully deleted"}