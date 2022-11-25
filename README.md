# Dressy Backend

# Start Server Dev
```shell
pipenv run dev
```

# Start Server Prod
con Nginx configurato per un proxypass 443:8000

```shell
sudo mkdir /var/run/gunicorn
sudo chown -R paola:paola /var/run/gunicorn
pipenv run prod
```


