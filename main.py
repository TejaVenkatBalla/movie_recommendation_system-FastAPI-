from fastapi import Depends
import numpy as np
import models
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"hello": "world"}

# user management


@app.post("/register")
async def register_user(username: str, db: Session = Depends(get_db)):
    User = models.User
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    new_user = User(username=username)
    db.add(new_user)
    db.commit()
    return {"username": username}


@app.get("/users")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"users": users}


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    db.commit()
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# movies management

@app.get("/movies")
async def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies")
async def create_movie(title: str, genre: str, db: Session = Depends(get_db)):
    new_movie = models.Movie(title=title, genre=genre)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, title: str, genre: str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = title
    movie.genre = genre
    db.commit()
    return {"message": "Movie updated successfully"}


@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}

# API route to rate a movie

@app.post("/movies/{movie_id}/rate")
async def rate_movie(user_id: int, movie_id: int, rating: float, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if movie exists
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Create movie rating
    movie_rating = models.MovieRating(
        user_id=user_id,
        movie_id=movie_id,
        rating=rating
    )
    db.add(movie_rating)
    db.commit()
    db.refresh(movie_rating)
    db.close()
    return movie_rating


# Collaborative Filtering Algorithm


def calculate_similarity(user_ratings_1, user_ratings_2):
    """
    Calculate cosine similarity between two users based on their ratings.

    Parameters:
        user_ratings_1 (List[float]): Ratings of user 1
        user_ratings_2 (List[float]): Ratings of user 2

    Returns:
        float: Cosine similarity between the two users

    """
    print("user ratings")
    print(user_ratings_1)
    print(user_ratings_2)
    # Convert ratings lists to numpy arrays
    ratings_1 = np.array(user_ratings_1)
    ratings_2 = np.array(user_ratings_2)
    # print(ratings_1,ratings_2)

    # Calculate dot product
    dot_product = np.dot(ratings_1, ratings_2)

    # Calculate magnitudes
    magnitude_1 = np.linalg.norm(ratings_1)
    magnitude_2 = np.linalg.norm(ratings_2)

    # Calculate cosine similarity
    if magnitude_1 != 0 and magnitude_2 != 0:
        similarity = dot_product / (magnitude_1 * magnitude_2)
    else:
        similarity = 0.0  # In case of division by zero

    return similarity


@app.get("/movies/{user_id}/rec")
def generate_recommendations(user_id: int, db: Session = Depends(get_db)):
    # Get user's ratings
    user_ratings = db.query(models.MovieRating).filter(
        models.MovieRating.user_id == user_id).all()
    all_ratings = db.query(models.MovieRating).all()

    user_ratings_dict = {
        rating.movie_id: rating.rating for rating in user_ratings}

    recommendations = []
    for rating in all_ratings:
        if rating.user_id != user_id:  # Exclude current user's ratings
            # Extract ratings for the compared user
            compared_user_ratings = db.query(models.MovieRating).filter(
                models.MovieRating.user_id == rating.user_id).all()
            compared_user_ratings_dict = {
                compared_rating.movie_id: compared_rating.rating for compared_rating in compared_user_ratings}

            # Construct rating vectors for both users
            user_ratings_vector = [user_ratings_dict.get(
                movie_id, 0) for movie_id in user_ratings_dict.keys()]
            compared_user_ratings_vector = [compared_user_ratings_dict.get(
                movie_id, 0) for movie_id in user_ratings_dict.keys()]  # Using keys from current user's ratings

            # Calculate similarity
            similarity_score = calculate_similarity(
                user_ratings_vector, compared_user_ratings_vector)

            print("sim score:", similarity_score)
            # If similarity score is above threshold, add recommendations
            if similarity_score > 0:
                recommendations.append((rating.movie_id, similarity_score))

    # Sort recommendations by similarity score
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Fetch movie names for recommendations
    movie_names = {}
    for movie_id, _ in recommendations:
        movie = db.query(models.Movie).filter(
            models.Movie.id == movie_id).first()
        if movie:
            movie_names[movie_id] = movie.title

    # Return recommendations with movie names
    recommendations_with_names = [(movie_names.get(
        movie_id, "Unknown")) for movie_id, similarity_score in recommendations]

    x = list(set(recommendations_with_names))
    return x
