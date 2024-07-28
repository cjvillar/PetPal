# PetPal

PetPal is a web application that connects people with pets to pet walkers and sitters. 
This project will demonstrate use of the FARM stack
(FastAPI for the backend, React (Remix) for the front end, and a dockerized MongoDB for the database.)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features
- User registration and authentication
- Pet listing and searching
- Booking requests for pet sitting or walking services
- User profiles and reviews

## Installation

### Prerequisites
- Docker
- Node.js
- Python 3.8+

### Backend Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/petpal.git
    cd PetPal/backend
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

### Frontend Setup
1. Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Install the required Node.js packages:
    ```bash
    npm install
    ```

3. Start the React development server:
    ```bash
    npm start
    ```

### Database Setup
1. Navigate to the database directory:
    ```bash
    cd ../database
    ```

2. Start the MongoDB container using Docker:
    ```bash
    docker-compose up -d
    ```

## Usage
1. Ensure the backend server, frontend server, and MongoDB container are running.
2. Open your browser and navigate to `http://localhost:3000` to access the PetPal application.
3. Register a new account or log in with an existing account.
4. Start listing pets or search for available petsitters/walkers.




