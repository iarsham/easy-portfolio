FROM python:3.10.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin
ENV DJANGO_SETTINGS_MODULE config.settings.production

WORKDIR /code
COPY ./requirements/* /code/
RUN pip install --upgrade pip && \
    pip install -r production.txt


CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@email.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi

EXPOSE 8000