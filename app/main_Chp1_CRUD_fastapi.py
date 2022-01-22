from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# request Get method url "/"
@app.get("/")
def root():
    return {"message": "Welcome to API!!!"}

my_posts = [{"title": "title of post1", "content": "content of post2", "id": 1},
            {"title": "favorite food", "content": "Pizza", "id": 2}
           ]

def find_post(id):
    for p in my_posts:
        if id == p['id']:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] ==id:
            return i

# request Get method url "/posts"
@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.get("/posts/latest")
def get_post():
    post = my_posts[len(my_posts)-1]
    return {"latest post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

# request Post method url "/posts"
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange (0, 1000000)
    print (post_dict)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete post
    #find the index in the array that has the required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    if index ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}