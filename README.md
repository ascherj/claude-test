# Blog API Project

A simple blog API built with FastAPI and SQLAlchemy that allows creating and retrieving blog posts and comments.

## Features

- RESTful API endpoints for blog posts and comments
- PostgreSQL database with SQLAlchemy ORM
- Sample data seeding
- Automatic API documentation via FastAPI

## Technical Stack

- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Relational database
- Pydantic - Data validation using Python type annotations

## Project Structure

- `main.py` - FastAPI application and route definitions
- `models.py` - SQLAlchemy database models
- `database.py` - Database connection and session management
- `seed.py` - Sample data generation script

## API Endpoints

- `GET /` - Redirects to index.html
- `GET /api/posts/` - Get all blog posts
- `GET /api/posts/{post_id}` - Get a specific blog post

## Development

This project (including this README) was developed using Claude 3.5 Sonnet (Anthropic) in the Cursor IDE. The AI assistant helped with code generation and project structuring while maintaining clean code practices and proper documentation.

## Getting Started

1. Install dependencies
2. Configure PostgreSQL connection in `database.py`
3. Run database migrations
4. Execute `seed.py` to populate sample data
5. Start the FastAPI server
