FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

WORKDIR /code
ADD requirements* /code/
RUN pip install --upgrade pip && \
    pip install -r production.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@email.com --noinput; \
    gunicorn -b 0.0.0.0:8000 backend.wsgi
