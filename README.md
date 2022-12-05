# Dressy Backend

```shell
pip install pipenv
pipenv install
pipenv install --dev
pipenv run mkm
pipenv run mkmapi
pipenv run migrate
pipenv run migrateapi
```

# pipenv first time
```shell
pipenv shell
nano .env # contenuto di questo sulla chat whatsapp
pip install pipenv && pipenv install && pipenv install --dev && pipenv run mkm && pipenv run mkmapi && pipenv run migrate && pipenv run migrateapi && pipenv run loadall
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

