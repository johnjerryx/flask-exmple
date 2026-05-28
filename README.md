# Flask, MySQL, SQLAlchemy, Celery, RabbitMQ, Redis, Nginx

This is a basic (but foundational) Flask app you can use to build your own application based on it. It has necessary foundations for:

- SQLAlchemy database connection
- SQLAlchemy `User` model with roles
- User authentication (using `Flask-Login`)
- Asynchronous background tasks (using Celery, RabbitMQ, and Redis)
- Nginx as a reverse proxy to handle external requests, terminate traffic safely, and shield the underlying Flask application layer.
- Fully containerized environment isolated cleanly through Docker Compose.

## First-Time Database Setup

Since this is a clean template, you need to initialize the database migration system and generate your core schema tables before launching the app for the first time:

```bash
   FLASK_ENV=local flask db init
```

## Database Migration:

To perform your database migrations locally (so that the migration files-which are part of your application files-will be pushed to your Git repository), run:

```bash
FLASK_ENV=local flask db migrate
```

## Deployment steps:

Before pushing to your production repository (the one you `pull` from in your VPS):

1. Uncomment the `#.env` line in the `.gitignore`.

On your VPS you should have separate, secure environment variables, with secure passwords.

2. Uncomment the `#.env.local` line in the `.gitignore`.

This file is used for your local development so that you will be able to run database migrations on your local development machine outside the Docker Container (it sets `MYSQL_HOST=localhost`).

3. Uncomment the `#docker-compose.override.yaml` line in the `.gitignore` .

The production `docker-compose.yaml` file's `web` service doesn't have an explicit `command`. Instead, its execution instruction defaults to Gunicorn inside the `Dockerfile`.

The `docker-compose.override.yaml` file overrides the `web` service for local development ease. Instead of `gunicorn`, it runs the Flask development server with the `--debug` flag set. It also mounts the application directory so that changes in your Flask app's code reflect immediately while the container is running.

> **Note on Celery:** While changes to your Flask code will live-reload instantly, Celery does not auto-reload code in memory. For any changes you make to the Celery worker or its tasks, you will need to restart the container, but a full image rebuild is not required:
> ```bash
> docker compose restart celery_worker
> 
> ```

## Running tests:

```
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up --build --abort-on-container-exit tester
```