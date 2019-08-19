* Overview

The switchapi project provides a web API that controls an attached coax RF
switch.  At the moment, the supported hardware for this project is a Beaglebone
Green Wireless for the control system and any switch that can be hooked up to
its ports.

Installation and configuration of the Beaglebone is left up to the user at this
point.  It is assumed some version of a Debian-derived operating system is
installed.  Make sure it is up-to-date.  A 9.x version is required to make sure
all the pins on the Beaglebone are supported.

The following packages and their dependencies need to be installed:

* python3-flask
* python3-flask-basicauth
* Adafruit_BBIO (install using pip3)
* uwsgi
* uwsgi-plugin-python3

* Configuration

At the moment, everything that could be configured is unfortunately coded right
into the source.  You should check the following things before installation:

* In `switchapi/BB.py`, the `self._gpioPinsUsed` variable is a list of which pins
on the Beaglebone are wired to the coax switch.  It is assumed that eight pins
will be used.  The defaults are known to work with a sufficiently recent operating
system version.  Change at your own risk.

* In `switchapi/__init__.py`, the line that creates a `BB` instance hardcodes a
list of transverters hooked up to the coax switch.  Exactly eight items must be
in this list.  Use `None` for anything that is not hooked up.  At the moment,
only transverters are really supported.

* In `switchapi/config.py`, the username and password are the credentials that
are used with the web API to do anything that touches hardware.  Change these
to whatever you want.  At the moment, HTTPS is not supported.  It is recommended
you only use this on a wireless network you control and that is not publically
available.

* Testing

From the tpo level source directory (the one with this file in it), the server
can be started like so:

```
$ FLASK_APP=switchapi flask run
```

You can then use curl to connect to port 5000 and get results back:

```
$ curl http://127.0.0.1:5000/active
{ "active": Nothing }
```

* Installation

switchapi expects to run right out of the source directory.  Simply configure the
user name, group name, and port in `coax-switch.service`.  Then install and enable
that just like any other systemd service:

```
# cp coax-switch.service /etc/systemd/system
# systemctl enable coax-switch.service
# systemctl start coax-switch.service
```

* API Routes

All API routes return their results as JSON objects.

* `/active` - Returns the band of the currently active port on the switch, or
`Nothing` if no port is active.

* `/config/bands` - Returns a list of all bands that can be selected on the switch.
Requires authentication.

* `/switch/<band>` - Attempts to switch to the given band.  Any of the values from
the `/config/bands` route are valid for this route.  Returns success or failure,
and a failure message if appropriate.  Requires authentication.
