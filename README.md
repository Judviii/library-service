# Library Service API

## Introduction
This project provides a Django-based API for managing books, borrowings and payments.
## Installation

### Prerequisites
Before you can run this project, make sure you have the following installed:

- Python 3.8 or higher
- Django 3.2 or higher
- pip (Python package installer)
- Docker (if you prefer running the API in a container)

### Running the API with Python
```shell
    git clone https://github.com/Judviii/library-service.git
    cd library_api
    
    # on macOS
    python3 -m venv venv
    source venv/bin/activate
    # on Windows
    python -m venv venv
    venv\Scripts\activate
    
    pip install -r requirements.txt
    
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
   
    (API will be available at http://127.0.0.1:8000/api/)
    python manage.py test
```

### Running the API with Docker
```shell
    git clone https://github.com/Judviii/library-service.git
    cd library_api

    # create an .env file in the root directory of project, use env.sample as example.

    docker-compose build
    docker-compose up
```
- Create new admin user. `docker-compose run app sh -c "python manage.py createsuperuser`;
- API will be available at http://127.0.0.1:8000/api/
- Get JWT token at http://127.0.0.1:8000/api/token/
- Run tests: `docker-compose run app sh -c "python manage.py test"`;