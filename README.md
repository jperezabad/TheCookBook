# TheCookBook
Web application to store cooking recipes.

## Usage

1. Download this repository.

2. Create an IMGUR anonymous API key in the following [site](https://api.imgur.com/oauth2/addclient). Paste the key in  in the parameter `IMGUR_CLIENT_ID` of the file `docker-compose.yml`.

3. Execute

```bash
$ docker-compose up
```

For security reasons, you may want to change some parameters in the file .

* `SECRET_KEY`

This is a common parameter used in several Flask plugings. It is used for example to protect forms against CSFR attacks. Execute this two commands in a Python terminal and copy and paste the result.

```python
>>> import os
>>> os.urandom(24)
```

* `DB_USER` and `DB_PASSWORD` 

User and password to access the MongoDB instance. This has to be the same parameters as `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD`
