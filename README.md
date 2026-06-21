# IHateToBudget

A small, self-hosted personal finance web app for tracking expenses, categories, and simple budgets.

This repository contains the IHateToBudget Django application. The project is intended for local or private hosting (e.g., Raspberry Pi, home server).

## Quick links

- Source: https://github.com/bminusl/ihatetobudget
- Project root: [README.md](README.md)

## Features

- Categorized expenses with monthly grouping (sheets)
- Simple budgeting and overviews
- Receipt attachment support (file storage)
- CSV data export for portability

Screenshots are available in the `screenshots/` directory.

## Supported setup (short)

- Recommended: Docker + Docker Compose
- Development: Pipenv (Python virtualenv)

## Installation

Choose one of the following methods.

### Docker (recommended)

1. Copy example files:

```bash
cp docker-compose.yml.example docker-compose.yml
cp docker-compose.env.example docker-compose.env
cp Caddyfile.example Caddyfile
```

2. Edit `docker-compose.env` (set `DJANGO_SECRET_KEY` and any currency variables).

3. Build and start:

```bash
docker compose up -d --build
```

4. Apply migrations and create a superuser (run inside the web container or use compose exec):

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

5. Start cron (if needed):

```bash
docker compose exec ihatetobudget service cron start
```

Visit the site at http://localhost:8000 (or the address configured in your compose file).

### Local development (Pipenv)

1. Install Pipenv and Python 3.8+ (project historically targets Python 3.8).

```bash
pipenv install --dev
pipenv shell
python manage.py migrate
python manage.py runserver
```

## Updating

When updating the codebase with Docker:

```bash
docker-compose down -v
git pull
docker-compose build
docker-compose run --rm ihatetobudget pipenv run python manage.py migrate
docker-compose up -d
```

Make a DB backup before upgrading (e.g., `cp db.sqlite3 db.sqlite3.bak`).

## Developer notes

- Code style: `black`, `flake8`, `isort` (pre-commit hooks recommended).
- Tests: run `python manage.py test` or `pytest` if installed.
- To check deployment settings: `python manage.py check --deploy`.

## Testing

Run unit tests:

```bash
python manage.py test
```

Measure coverage (optional):

```bash
coverage run --source='.' manage.py test
```

## Contributing

Contributions are welcome via issues and pull requests. Please follow repository conventions (pre-commit hooks) and keep changes focused.

See `CONTRIBUTING.md` (if present) or open an issue to discuss larger changes before implementing.

## License

See `COPYING` for license terms.

---

If you'd like, I can further condense sections, re-add badges, or generate a short changelog summary for the README.
  ```

* Alternatively, [`coverage`](https://pypi.org/project/coverage/) can be used to measure code coverage:

  ```bash
  coverage run --source='.' manage.py test
  ```
