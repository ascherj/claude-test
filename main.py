from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db
from datetime import datetime
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic models for request/response
class PostBase(BaseModel):
    title: str
    content: str
    author: str

class CommentBase(BaseModel):
    content: str
    author: str

class Post(PostBase):
    id: int
    created_at: datetime
    comments: List[CommentBase] = []

    class Config:
        orm_mode = True

# API Routes
@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")

@app.get("/api/posts/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/api/posts/")
def create_post(post: PostBase, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.post("/api/posts/{post_id}/comments/")
def create_comment(post_id: int, comment: CommentBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = models.Comment(**comment.dict(), post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Serve static files
app.mount("/", StaticFiles(directory="static"), name="static")
