# First4Aid

![A demonstration of a the First4Aid app](https://tkachikoti-cloud-object-storage.ams3.digitaloceanspaces.com/images/github/first4aid/first4aid-register-and-login.gif)

This repository contains a containerised application designed to support the facilitation of humanitarian aid services.


## Table of contents

- [Description](#description)
- [Installing and running the app](#installing-and-running-the-app)
- [Uninstalling and Shutting down the app](#uninstalling-and-shutting-down-the-app)
- [Testing the app](#testing-the-app)
- [Functionality overview](#functionality-overview)

## Description

This repository contains a synchronous microservice architecture project built using Python-based minimal web framework [Flask](https://github.com/pallets/flask).
- The microservice architecture was implemented using [Docker Engine](https://github.com/docker) container run-time with [Python 3.9](https://github.com/python/cpython) running on the security-oriented Linux distribution [Alpine Linux](https://github.com/docker).
- The front end interface was built using [Bootstrap](https://github.com/twbs/bootstrap) for HTML/CSS components, [Jinja](https://github.com/pallets/jinja) for the template engine.
- The database was implemented using [PostgreSQL](https://github.com/postgres) (SHA-512 encrypted data) with [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy) for Object-relational mapping and [Psycopg](https://github.com/psycopg/psycopg2) for the database adapter.
- The security features were implemented using [Flask-Login](https://github.com/maxcountryman/flask-login) for user session management, [Flask-Bcrypt](https://github.com/maxcountryman/flask-bcrypt) for the authentication related hashing utilities, [PyJWT](https://github.com/jpadilla/pyjwt) for secure JSON Web Token implementation and [Flask-WTF](https://github.com/wtforms/flask-wtf) for CSRF and file upload integration.
- The testing functionality was implemented using [pytest](https://github.com/pytest-dev/pytest).

## Installing and running the app

1. Download, install and run Docker Desktop: https://www.docker.com/products/docker-desktop/

2. Clone the repository to your local machine:

```
$ git clone https://github.com/Least-Privilege-Team/first4aid_final
```

3. Change directory to access root directory:

```
$ cd first4aid_final
```

4. Build and initialise the app - this step might take a few minutes to complete:

```
$ docker-compose up -d
```

5. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a web browser.

## Testing the app

1. After following the installation process, tests are executed by entering:

```
$ docker exec -i flask_app pytest
```

## Uninstalling and shutting down the app

1. From the root directory execute the following command:

```
$ docker-compose down --rmi all
```

## Functionality overview

### Authentication