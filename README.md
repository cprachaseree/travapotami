# travapotami

## Dependencies

* flask
* flask-sqlalchemy
* mysqlclient

## Start a Development Server

All the dependencies should be install. 

MySQL database server must be running. The username, password, and database name can be set in __init__.py under 'SQLALCHEMY_DATABASE_URI'

```
SQLALCHEMY_DATABASE_URI='mysql://username:password@localhost/travapotami'
```


While being in the repo directory, in Mac or Linux terminal, type

```
$ export FLASK_APP=travapotami
$ flask run
```

In Windows cmd, type

```
set FLASK_APP=travapotami
flask run
```

When running the app for the first time, initialize the database by

```
flask init-db
```

This will create the table according to models.py

localhost:5000/hello should return "Hello World!" and localhost:5000/bye should return "Bye World!"
