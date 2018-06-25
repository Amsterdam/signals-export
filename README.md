# Signals export
Service that sends the required messages to external APIs. This belongs to the
Signalen in Amsterdam project. Related code:
* [Central backend application for "Signalen in Amsterdam"](https://github.com/Amsterdam/signals)
* [Front-end code for "Signalen in Amsterdam"](https://github.com/Amsterdam/signals-frontend)

## Prerequisites

* `docker-compose`


## Running the code

*Note: this code is still very much work in progress.*

This project comes with a docker-compose file that will build a self contained development
environment (with bind mounts for the web application source).

Set the `SIGMAX_SERVER` and `SIGMAX_AUTH_TOKEN` environment variables to appropriate
values (these are secret, so not included with the source).

```sh
docker-compose up --build
```

The service will now run on http://localhost:8000/signals_export , complete with Redoc documentation
on http://localhost:8000/signals_export/redoc/.

## Running the test suite

``sh
docker-compose run web --rm python manage.py test
``
