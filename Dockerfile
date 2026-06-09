FROM python:3.10


ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY=change-me

WORKDIR /usr/src/app

COPY . .

# Note: Rust is required by `cryptography` (python package)
RUN apt-get update && apt-get -y install cron rustc

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run python manage.py collectstatic --noinput

RUN pipenv run python manage.py crontab add
