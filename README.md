# Movie Recommendation System
## Table of Contents
 
- [Description](#description)
- [Setup](#setup)
- [Run](#run)
- [API Documentation](#api-documentation)
- [Contact](#contact)
 
## Description
 
This project is a FastAPI backend application that provides movie recommendations based on user preferences. The API allows users to register, log in, rate movies, and receive personalized recommendations. The recommendations are generated using collaborative filtering techniques.
 
## Setup
To use Movie Recommendation System use below repo
 

```
git clone https://github.com/TejaVenkatBalla/movie_recommendation_system-FastAPI-.git
cd your-repo
```

It is recommended to create virtual environments while installing Python applications

For Windows,

* Create virtual environent using `python -m venv "path"`
* Activate virtual envrionment using `venv\Scripts\activate.bat`

For Linux, 
* Create virtual environment using `virtualenv venv`
* Activate using source `venv/bin/activate`

## Run

To run server
```
uvicorn main:app --reload
```

## API Documentation
Link to the [Postman Collection](https://github.com/TejaVenkatBalla/movie_recommendation_system-FastAPI-/blob/main/Movie_recommendation_system.postman_collection.json)

### User Management Endpoints
- **Create a new user:** POST `/register?username={username}`
- **List all users:** GET `/users`
- **Retrieve a specific user's details:** GET `/users/{user_id}`
- **Update a user's details:** PUT `/users/{user_id}?username={new_username}`
- **Delete a user:** DELETE `/users/{user_id}`

### Movie Management Endpoints
- **List all movies:** GET `/movies/`
- **Retrieve details of a specific movie:** GET `/movies/{movie_id}`
- **Create a new movie:** POST `/movies/?title={title}&genre={genre}`
- **Update a movie's details:** PUT `/movies/{movie_id}?title={new_title}&genre={new_genre}`
- **Delete a movie:** DELETE `/movies/{movie_id}`

### Recommendation System Endpoints
- **Rate a movie:** POST `/movies/{movie_id}/rate?user_id={user_id}&rating={rating}`
- **Get movie recommendations:** GET `/movies/{movie_id}/rec`

## Contact
Email: tejavenkatballa@gmail.com
contact: +91 9539530165 
