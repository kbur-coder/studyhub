# StudyHub

A platform where students publish their projects: register, fill in a profile, add projects with a description, technologies, a link and a screenshot, and browse what other students built.

## Features

- Registration, login and logout
- Projects with title, description, technologies, external link and image (images are shrunk automatically)
- Only the author can edit a project
- User profiles with avatar, bio, location, website and GitHub username
- Dark GitHub-style interface in Russian

## Stack

Django 5.2, PostgreSQL in production and SQLite locally, WhiteNoise for static files, Pillow for images, gunicorn.

## Run locally

Requirements: Python 3.12 or newer.

    git clone https://github.com/kbur-coder/studyhub.git
    cd studyhub
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

On Linux and macOS use `source venv/bin/activate` and `cp .env.example .env`. Open http://127.0.0.1:8000.

## Settings

All settings come from environment variables, or from a `.env` file next to `manage.py`.

| Variable | Meaning |
| --- | --- |
| `SECRET_KEY` | required when `DEBUG` is off |
| `DEBUG` | `True` for local development, anything else means production |
| `DATABASE_URL` | Postgres connection string. SQLite is used when empty |
| `ALLOWED_HOSTS` | comma separated host names |
| `CSRF_TRUSTED_ORIGINS` | comma separated origins such as `https://example.com` |

## Tests

    python manage.py test

## Deploy on Render

`render.yaml` describes the web service and a free Postgres database.

1. Push the repository to GitHub.
2. In Render choose **New**, **Blueprint** and select the repository.
3. Render creates the service, generates `SECRET_KEY`, connects the database and runs migrations during the build.
4. Create the first admin account in the Render shell: `python manage.py createsuperuser`.

Limits of the free plan: the service sleeps after inactivity, and uploaded images are stored on a disk that is wiped on every deploy. For permanent storage connect an object store such as Cloudinary or S3.

## Why not Netlify

Netlify hosts static sites and serverless functions. StudyHub is a Django application with a database and user uploads, so it needs a server process and cannot run there. A static front end for Netlify would need a separate backend or a rewrite on a service such as Supabase.

## Structure

    backend/        project settings and URLs
    projects/       models, views, forms, templates and tests
    static/         css
    render.yaml     deployment blueprint
