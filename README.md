The system will manage events, attendees, venues, ticket bookings, and multimedia assets, including event posters (images),
promotional videos, and venue photos.

## Features

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate (or .venv\Scripts\activate on Windows)
```

2. Install dependencies:

FastAPI - A modern, fast (high-performance) web framework for building APIs.
```bash
pip install fastapi
```

Uvicorn - A lightning-fast ASGI server implementation, using uvloop and httptools. 
```bash
pip install uvicorn
```

Motor - The async driver for MongoDB, designed to work with Tornado or asyncio. 
```bash
pip install motor
```

Pydantic - Data validation and settings management using Python type annotations. 
```bash
pip install pydantic
```

Python-dotenv - Reads key-value pairs from a .env file and can set them as environment variables. 
```bash
pip install python-dotenv
```

Requests - A simple, yet elegant HTTP library for Python, built for human beings. 
```bash
pip install requests
```

3. Create a requirement.txt
```bash
pip freeze > requirements.txt
```

## Running the Application

1. Start the Server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8000
```
