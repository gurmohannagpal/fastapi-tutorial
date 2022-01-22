from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='password') #, cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Database connection was successful!")
        break

    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


# request Get method url "/"
@app.get("/")
def root():
    return {"message": "Welcome to API!!!"}

# request Get method url "/posts"
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    print (posts)
    return {"data" : posts} 

@app.get("/posts/latest")
def get_post():
    post = my_posts[len(my_posts)-1]
    return {"latest post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# request Post method url "/posts"
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #this is better implementation
    cursor.execute("""INSERT INTO posts (title, content, published)
                      VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data" : new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                      (post.title, post.content, post.published, str(id)) )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {'data': updated_post}