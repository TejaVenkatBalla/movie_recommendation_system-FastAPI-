from sqlalchemy import Column, Integer, String, Float, CheckConstraint, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import json


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    # Relationship to rated movies
    rated_movies = relationship("MovieRating", back_populates="user")


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String, index=True)

    # Relationship to users who rated the movie
    rated_by_users = relationship("MovieRating", back_populates="movie")


class MovieRating(Base):
    __tablename__ = 'movie_rating'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Float)

    # Define relationship to User and Movie
    user = relationship("User", back_populates="rated_movies")
    movie = relationship("Movie", back_populates="rated_by_users")
