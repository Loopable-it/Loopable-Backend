<p style="text-align: center;">
  <img alt="loopable logo" src="https://user-images.githubusercontent.com/32592671/229338661-84ae1264-a7e0-4205-b584-10b56f0d9382.png" />
</p>

# The product
LOOPABLE is a platform that promotes the circular economy and environmental sustainability with the rental of objects between private individuals. Users reduce the environmental impact of the production of goods intended for little use, earning through the rental of the objects they own. It allows responsible management of resources and the reduction of waste, contributing to a more sustainable future.

## Backend
This is a Django Rest Framework project for https://loopable.it.

## Run the project
To run the project, you need to have at least Python 3.9 installed on your machine. 
Then, you need to install the dependencies in a new virtual environment with the following command:
```bash
python3 -m venv env
source env/bin/activate # On Linux
env\Scripts\activate # On Windows
pip install -r requirements.txt
```

To run the project **make sure to have all the environment variables set**. You can find them in the `.env.example` file. 
Then, you can run the project with the following command:
```bash
python3 src/manage.py runserver 8000
```

## Run the tests
To run the tests, you need to have the project running and then run the following command:
```bash
python3 src/manage.py test -v 2
```

## Migration
To run the migration, you need to have the project running and then run the following command:
```bash
python3 src/manage.py makemigrations
python3 src/manage.py migrate
```
