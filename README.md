# website

My website

## Installation

Pre-requisites:

1. Install Python 3
1. Install pip 3
1. Install virtualenv: `pip3 install virtualenv`

Execute the following commands in the root directory of the project.

1. Create the virtual environment: `virtualenv venv`
1. Activate virtualenv: `source venv/bin/activate`
1. Install django: `python -m pip3 install Django`
1. Install dependencies: `pip3 install -r requirements.txt`

## How to run?

### Development

1. Start Docker compose: `docker-compose up -d`
1. Add user to database
   1. `psql -h localhost -p 5432 -U postgres`
   1. `CREATE DATABASE websitedb;`
   1. `CREATE USER websiteuser WITH ENCRYPTED PASSWORD 'password';`
   1. `GRANT ALL PRIVILEGES ON DATABASE websitedb TO websiteuser;`
   1. `\q`
1. Run migrations: `python manage.py migrate`
1. Start server: `python manage.py runserver`

## Supported URLs

* http://localhost:8000/about
* http://localhost:8000/users/login
* http://localhost:8000/admin

## How does the blog work?

See: [Blog README](./blog/README.md)
