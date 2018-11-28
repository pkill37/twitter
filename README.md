# twitter

## Development

Sync the database for the first time

```
python manage.py migrate
```

Create initial user

```
python manage.py createsuperuser --email fabio.maia@fer.hr --username fabio
```

Run the server

```
python manage.py runserver
```

Try to login

```
curl -H 'Accept: application/json; indent=4' -u fabio:demo1234 http://127.0.0.1:8000/users/
```

## Tests

Run tests

```
python manage.py tests --parallel
```
