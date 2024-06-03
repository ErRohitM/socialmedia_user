# Social Networking Application API

## Overview

This is a social networking application API built with Django Rest Framework. The API allows users to sign up, log in, search for other users, send/accept/reject friend requests, list friends, and list pending friend requests.

## Features

- User Registration
- User Login
- Search Users
- Send Friend Requests
- Accept/Reject Friend Requests
- List Friends
- List Pending Friend Requests

## Installation

### Prerequisites

- Python 3.8+
- pip
- Docker
- Docker Compose

### Steps

1. **Clone the repository**:

    ```sh
    git clone https://github.com/ErRohitM/socialmedia_user.git
    cd socialmedia_user
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate 
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```sh
    python manage.py migrate
    ```

5. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

### Docker Setup

To run the application in a Docker container:

1. **Build and run the containers**:

    ```sh
    docker-compose up --build
    ```

2. **Access the application**:

    The application will be available at `http://127.0.0.1:8000`.

## Postman Collection
You can find the Postman collection for testing the API endpoints [here](https://github.com/ErRohitM/socialmedia_user/blob/main/socialmedia-user-postman_collection.json).

## API Endpoints

### Signup

POST /api/signup/


### Login

POST /api/login/


### Search Users

GET /api/search/?search=<keyword>


### Send Friend Request

POST /api/friend-request/send/


### Accept Friend Request

POST /api/friend-request/accept/<friend_request_id>/


### Reject Friend Request

POST /api/friend-request/reject/<friend_request_id>/


### List Friends

GET /api/friends/


### List Pending Friend Requests

GET /api/friend-requests/pending/

