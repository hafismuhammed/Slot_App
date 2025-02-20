# Interview Slot APIs

This Django-based REST API allows candidates and interviewers to register their available time slots and find common available slots for scheduling interviews. The project includes Swagger documentation for API reference and supports Docker for easy deployment.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Provide instructions and examples for using your project.

## Running Locally

1. Ensure your virtual environment is activated:
    ```sh
    source env/bin/activate
    ```

2. Apply migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Run the development server:
    ```sh
    python manage.py runserver
    ```

4. Open your browser and navigate to `http://127.0.0.1:8000/`.

## Running with Docker

1. Build and Run the project:
    ```sh
    docker-compose up -d --build.
    ```

Base URL `http://127.0.0.1:8000/`.

Swagger UI: `http://127.0.0.1:8000/swagger/`

## Environment Variables

Create a .env file in the root directory with the following:
 ```sh
    DB_NAME='your_db_name'
    DB_USER='your_db_user'
    DB_PASSWORD='your_db_user'
```