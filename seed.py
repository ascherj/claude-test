from database import SessionLocal
from models import Post, Comment
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()

    # Clear existing data
    db.query(Comment).delete()
    db.query(Post).delete()

    # Create sample posts
    posts = [
        Post(
            title="Welcome to the Blog",
            content="This is our first blog post! We're excited to share our thoughts and ideas with you.",
            author="Admin",
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
        Post(
            title="The Art of Programming",
            content="Programming is both a science and an art. It requires logical thinking and creative problem-solving skills. In this post, we'll explore what makes programming such a unique discipline.",
            author="Jane Doe",
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        Post(
            title="Python vs JavaScript: A Friendly Comparison",
            content="Both Python and JavaScript are incredibly popular programming languages, each with its own strengths. Let's explore the key differences and similarities between these two languages.",
            author="John Smith",
            created_at=datetime.utcnow() - timedelta(days=1)
        )
    ]

    # Add posts to database
    for post in posts:
        db.add(post)
    db.commit()

    # Add comments to posts
    comments = [
        Comment(
            content="Great first post! Looking forward to more content.",
            author="User123",
            post_id=1,
            created_at=datetime.utcnow() - timedelta(days=4)
        ),
        Comment(
            content="This is exactly what I needed to read today.",
            author="ProgrammingFan",
            post_id=2,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        Comment(
            content="Interesting comparison! Could you also add some code examples?",
            author="CodeNewbie",
            post_id=3,
            created_at=datetime.utcnow() - timedelta(hours=12)
        ),
        Comment(
            content="I agree with your points about programming being an art!",
            author="DevArtist",
            post_id=2,
            created_at=datetime.utcnow() - timedelta(days=1)
        )
    ]

    # Add comments to database
    for comment in comments:
        db.add(comment)
    db.commit()

    db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed_database()
    print("Database seeded successfully!")
