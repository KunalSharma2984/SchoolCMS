# Contributing

Thanks for taking a look at the project.

## Local workflow

1. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`.
3. Run migrations with `python manage.py migrate`.
4. Make a focused change and add a regression test when behavior changes.
5. Run `python manage.py test` and `python manage.py check` before opening a pull request.

Keep pull requests small enough to review. Please describe what changed, how it was tested, and any setup detail a reviewer needs.
