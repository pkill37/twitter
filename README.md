# twitter

A simple RESTful API of a Twitter clone developed in the context of a Service-Oriented Computing class at the Faculty of Electrical Engineering and Computing of the University of Zagreb.

## Install

Install dependencies:

```
pip install -r requirements.txt
```

## Development

Sync the database:

```
python manage.py migrate
```

Create superuser:

```
python manage.py createsuperuser --email fabio.maia@fer.hr --username fabio
```

Run the development server:

```
python manage.py runserver
```

## Tests

Run tests:

```
python manage.py tests --parallel
```

## Documentation

See automatically generated documentation at `/swagger` or `/redoc`.
