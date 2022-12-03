# Dressy Backend

```
pip install pipenv
pipenv install
pipenv install --dev
pipenv run mkm
pipenv run mkmapi
pipenv run migrate
pipenv run migrateapi
```

```
pip install pipenv && pipenv install && pipenv install --dev && pipenv run mkm && pipenv run mkmapi && pipenv run migrate && pipenv run migrateapi
```

# Start Server Dev

```shell
pipenv run dev
```

# Start Server Prod

con Nginx configurato per un proxypass 443:8000

```shell
pipenv run prod
```

# Requirements

- [x] Setup git repositories
- [x] Setup Django REST Framework with CORS and documentation
- [x] Define at least one model (don’t overdo)
- [x] Expose your models with your API in a proper way (validate incoming data)
- [x] Implement authentication and authorization in a proper way
- [x] Test the back-end (coverage of your code >90%)
