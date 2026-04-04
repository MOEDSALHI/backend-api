# Project Setup Guide

This guide provides step-by-step instructions to set up and test the API on a local machine.

## 1. Clone the Repository
```sh
git clone https://github.com/MOEDSALHI/backend-api.git
cd backend-api
```

## 2. Install Dependencies
Ensure you have Poetry installed, then run:
```sh
poetry install
```

## 3. Set Up Environment Variables
Copy the example environment file and rename it:
```sh
cp .env.dist .env
```
Then, edit the `.env` file if necessary:
```ini
POSTGRES_DB=backend_db
POSTGRES_USER=backend_user
POSTGRES_PASSWORD=backend_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
DEBUG=True
SECRET_KEY=your_secret_key
```

## 4. Start the Project with Docker
```sh
docker-compose down -v
docker-compose up --build -d
```
This will start the PostgreSQL database and Django application in separate containers.

## 5. Run Migrations
```sh
docker exec -it django_app poetry run python manage.py migrate
```

## 6. Collect Static Files
```sh
docker exec -it django_app poetry run python manage.py collectstatic
```

## 7. Create a Superuser
```sh
docker exec -it django_app poetry run python manage.py createsuperuser
```
Follow the prompts to create an admin user.

## 8. Add User Groups via Django Admin
After logging into Django Admin, navigate to `Authentication and Authorization > Groups` and create the following groups:
- **Clients**
- **Staff**

## 9. Start the Development Server
If not already running, you can start Django manually:
```sh
docker exec -it django_app poetry run python manage.py runserver 0.0.0.0:8000
```

## 10. Access the API

- **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Authentication:**
  - `POST /api/auth/login/` (Login and obtain tokens)
  - `POST /api/auth/logout/` (Logout and blacklist token)
  - `POST /api/auth/refresh/` (Refresh token)
- **Bar API Endpoints:**
  - `GET /api/bar/references/` (List all beer references)
  - `GET /api/bar/bars/` (List all bars)
  - `GET /api/bar/stocks/` (View stock levels)
  - `POST /api/bar/orders/` (Create an order, requires authentication)

## 11. Running Tests
To run tests using `pytest`:
```sh
docker exec -it django_app poetry run pytest
```

## 12. Formatting & Linting
Ensure code consistency by running:
```sh
docker exec -it django_app poetry run isort .
docker exec -it django_app poetry run black .
```

Your API is now set up and ready for testing! 🚀