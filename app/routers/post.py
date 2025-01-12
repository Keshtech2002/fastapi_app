from .. import models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from ..schemas import PostBase, PostCreate, Post, UserCreate, UserOut
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[Post])
def get_post(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db:Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published)
    # )
    
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# title str, content str



@router.get("/{id}", response_model=Post)
def get_post(id: int, response: Response, db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts where id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):

    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
   
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db:Session = Depends(get_db)):

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id))
    # )

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()