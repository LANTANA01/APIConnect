from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
"""A CRUD application development"""

class Post(BaseModel):
    title: str  # Title of the post
    content: str  # Content of the post
    published: bool = True  # Whether the post is published (default: True)
    rating: Optional[int] = None  # Optional rating for the post

My_posts = [
    {"title": "Aiaha Tijani", "content": "aishtj@gmail.com", "id": 1},
    {"title": "Jemilah Tijani", "content": "jemtj@gmail.com", "id": 2},
]

def find_post(id: int):
    """
    Find a post by its ID.
    """
    for post in My_posts:
        if post['id'] == id:
            return post

def find_post_index(id: int):
    """
    Find the index of a post by its ID.
    """
    for i, p in enumerate(My_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    """
    Root endpoint. Welcome message.
    """
    return {"message": "Welcome to APIConnect!"}

@app.get("/posts")
def get_post():
    """
    Get all posts.
    """
    return {"message": My_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Create a new post.
    """
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    My_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    """
    Get the latest post.
    """
    post = My_posts[-1]
    return {"data": f"Latest Post: {post}"}

@app.get("/posts/{id}")
def get_single_post(id: int):
    """
    Get details of a single post by its ID.
    """
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id of {id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Delete a post by its ID.
    """
    post_index = find_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with an id of {id} does not exist.")
    My_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """
        Update a post by its ID.
    """
    post_index = find_post_index(id)
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with an id of {id}")
    post_dict = post.dict()
    post_dict['id'] = id
    My_posts[post_index] = post_dict
    return {"detail": post_dict}

