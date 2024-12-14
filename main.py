from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import List
from datetime import datetime
from pydantic import BaseModel
from database import get_db

app = FastAPI()

# Create tables if they don't exist
def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            author VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            post_id INTEGER REFERENCES posts(id)
        );
    """)
    conn.commit()
    cur.close()

# Initialize database tables
conn = get_db()
create_tables(conn)
conn.close()

# Pydantic models remain the same
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

@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")

@app.get("/api/posts/")
def get_posts(conn = Depends(get_db)):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*,
            COALESCE(json_agg(
                json_build_object(
                    'content', c.content,
                    'author', c.author,
                    'created_at', c.created_at
                )
            ) FILTER (WHERE c.id IS NOT NULL), '[]') as comments
        FROM posts p
        LEFT JOIN comments c ON p.id = c.post_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """)
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int, conn = Depends(get_db)):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*,
            COALESCE(json_agg(
                json_build_object(
                    'content', c.content,
                    'author', c.author,
                    'created_at', c.created_at
                )
            ) FILTER (WHERE c.id IS NOT NULL), '[]') as comments
        FROM posts p
        LEFT JOIN comments c ON p.id = c.post_id
        WHERE p.id = %s
        GROUP BY p.id
    """, (post_id,))
    post = cur.fetchone()
    cur.close()
    conn.close()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/api/posts/")
def create_post(post: PostBase, conn = Depends(get_db)):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO posts (title, content, author)
        VALUES (%s, %s, %s)
        RETURNING id, title, content, author, created_at
    """, (post.title, post.content, post.author))
    new_post = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_post

@app.post("/api/posts/{post_id}/comments/")
def create_comment(post_id: int, comment: CommentBase, conn = Depends(get_db)):
    # First check if post exists
    cur = conn.cursor()
    cur.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()

    if post is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")

    cur.execute("""
        INSERT INTO comments (content, author, post_id)
        VALUES (%s, %s, %s)
        RETURNING id, content, author, created_at, post_id
    """, (comment.content, comment.author, post_id))
    new_comment = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_comment

# Serve static files
app.mount("/", StaticFiles(directory="static"), name="static")
