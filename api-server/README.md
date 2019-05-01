The api-server is built on top of python-flask.  Install python-flask either
through your distribution's packaging system or with pip.  The former will
create /usr/bin/flask, while the latter will create ~/.local/bin/flask.  Then,
you can run the api-server on the command line line so:

```
$ FLASK_APP=switcherapi flask run
```

You can test out any of the GET routes with curl:

```
$ curl http://127.0.0.1:5000/active
Nothing active
```

You can also test out the POST routes with curl:

```
$ curl -X POST -F "freq=446.00" http://127.0.0.1:5000/freq/IC-7000
Set frequency on IC-7000 to 446.0
```

For now, nothing actually does anything so you can provide any values you'd
like and will almost certainly just get dummy values back.
