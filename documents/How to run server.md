## Run Server

### By Docker

```
docker-compose down && docker-compose up -d
```

### By Terminal

```
# Running DB by Docker
docker-compose down && docker-compose up -d db

# Running Server
python manage.py runserver
```