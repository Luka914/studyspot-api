
# StudySpot API

A RESTful API built with Python and FastAPI
that allows users to discover, filter and
manage study spaces.

<img width="1273" height="719" alt="swagger ui of studyspots api" src="https://github.com/user-attachments/assets/66c08fd0-0182-4bbf-9bb5-faebee735722" />


## Installation

Clone the repository:

    git clone [YOUR_GITHUB_REPOSITORY_URL](https://github.com/Luka914/studyspot-api.git)

Enter the project directory:

    cd studyspot-api

Create a virtual environment:

    python -m venv venv

Activate the environment.

Install dependencies:

    pip install -r requirements.txt

## Running the API

Run:

    uvicorn main:app --reload

Open:

    http://127.0.0.1:8000

## Testing

Run automated tests:

    python -m pytest -v

<img width="1625" height="674" alt="testing_api" src="https://github.com/user-attachments/assets/49fac72c-f757-4ed1-8eb9-41e5061f11a8" />


## API Documentation

Interactive documentation:

    http://127.0.0.1:8000/docs

Alternative documentation:

    http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API homepage |
| GET | /spots | Get all study spaces |
| GET | /spots/{id} | Get one study space |
| POST | /spots | Create a study space |
| PUT | /spots/{id} | Update a study space |
| DELETE | /spots/{id} | Delete a study space |

## Future Improvements

- Add student reviews and ratings
- Add user authentication
- Add pagination
- Add more advanced filtering
- Deploy the API online
