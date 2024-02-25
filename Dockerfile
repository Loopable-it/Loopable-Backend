FROM python:3.12
LABEL authors="AnonymousGCA"

WORKDIR /code
EXPOSE 8000

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    git \
    -y

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .env ./

COPY ./src ./src

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
