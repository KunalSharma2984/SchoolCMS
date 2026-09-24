# Student Management System

A small Django app for keeping course work in one place. Students can join courses, submit assignments, and check grades. Teachers can create courses, review submissions, and record grades. The project uses Django templates and a little plain CSS so the moving parts stay easy to follow.

## Built with

- Python 3.10+
- Django 4.2
- SQLite for local development
- Django templates and CSS

## Run it locally

1. Clone the repository and open the project directory.
2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    python -m pip install -r requirements.txt
    ```

4. Copy `.env.example` to `.env` and replace `SECRET_KEY` with a long random value. On Windows PowerShell, use `Copy-Item .env.example .env`.
5. Create the local database:

    ```bash
    python manage.py migrate
    ```

6. Start the server:

    ```bash
    python manage.py runserver
    ```

Open http://127.0.0.1:8000/ in a browser. Create your own administrator with `python manage.py createsuperuser`, or load the demo records with `python manage.py seed`.

## Demo data

The seed command is intended for local demos only. It creates one admin, two teachers, two students, three courses, and a few assignments. The command does nothing when the `admin` demo account already exists.

The demo passwords are printed by the command after it runs. Do not use them for a real deployment.

## Tests and checks

Run the same checks used by CI:

```bash
python manage.py test
python manage.py check
```

## Configuration

The repository intentionally keeps deployment configuration small. Set these values in `.env` or in the hosting provider's environment:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django signing key; required in every environment |
| `DEBUG` | Set to `False` outside local development |
| `ALLOWED_HOSTS` | Comma-separated host names |
| `SECURE_SSL_REDIRECT` | Set to `True` when HTTPS is configured |

The default database is SQLite. For production, configure a managed database and update the `DATABASES` setting for the deployment environment.

## Useful pages

- `/login/` and `/register/` for accounts
- `/dashboard/` for the role-specific home page
- `/courses/` for courses and assignments
- `/admin/` for Django's admin site

## Project layout

`accounts/` contains the custom user model and authentication views. `courses/` contains courses, assignments, submissions, and grades. Templates live in `templates/`, styles in `static/`, and the small demo loader is `accounts/management/commands/seed.py`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the short development workflow and [SECURITY.md](SECURITY.md) for reporting security issues.
