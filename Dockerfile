FROM python:3.12 as builder

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# Base
FROM python:3.12-slim as base

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update -y && apt-get install -y \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

ADD src /app


# Test Django
FROM base as test_django
CMD python /app/manage.py test -v 2 && echo "Django tests passed!"


# Check Pylint
FROM base as check_pylint
ADD pylintrc /app/pylintrc
CMD export PYTHONPATH=/app && pylint /app/ --rcfile=/app/pylintrc && echo "Pylint passed!"


# Check Flake8
FROM base as check_flake
ADD flake8 /app/flake8
CMD flake8 /app/ --config=/app/flake8 --show-source --statistics && echo "Flake8 passed!"


# Development with hot reload and mounted volume on /devel
FROM base as devel

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
# Mount the volume on /devel
CMD python /devel/manage.py migrate && python /devel/manage.py runserver 0.0.0.0:8000


# Production
FROM base as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
CMD python /app/manage.py collectstatic && python /app/manage.py migrate \
    && gunicorn --chdir /app/ loopable.wsgi:application --bind 0.0.0.0:8000 \
    --timeout=10 --access-logfile=- --error-logfile=-
