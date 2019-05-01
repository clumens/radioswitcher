from flask import Flask, jsonify, request
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/active")
    def active():
        # Return the currently active device (port, antenna, transverter, radio)
        return "Nothing active"

    @app.route("/config")
    def config():
        # Return the complete configuration of the switch
        return "Nothing configured"

    @app.route("/config/antennas")
    def config_antennas():
        # Return just the configured antennas
        return "No antennas"

    @app.route("/config/ports")
    def config_ports():
        # Return just the configured ports
        return "No ports"

    @app.route("/config/radios")
    def config_radios():
        # Return just the configured radios
        return "No radios"

    @app.route("/config/transverters")
    def config_transverters():
        # Return just the configured transverters
        return "No transverters"

    @app.route("/freq/<radio>", methods=["GET", "POST"])
    def freq(radio):
        if request.method == "POST":
            mode = request.form['freq']
            return "Set frequency on %s to %s" % (radio, mode)
        else:
            return "Frequency of %s is 146.52" % radio

    @app.route("/get/<device>", defaults={"key": ""})
    @app.route("/get/<device>/<key>")
    def get_device_key(device, key):
        # Return a config parameter about a particular device.  If no key is given, return everything.
        if key == "":
            return "No devices"
        else:
            return "No devices"

    @app.route("/log", methods=["POST"])
    def log():
        local_call = request.form['local_call']
        remote_call = request.form['remote_call']
        xc_sent = request.form['xc_sent']
        xc_rcvd = request.form['xc_rcvd']
        return "Can't log"

    @app.route("/set/<device>/<key>/<value>", methods=["POST"])
    def set_device_key(device, key, value):
        # Set a config parameter on a particular device.
        return "%s = %s" % (key, value)

    @app.route("/mode/<radio>", methods=["GET", "POST"])
    def mode(radio):
        if request.method == "POST":
            mode = request.form['mode']
            return "Set mode on %s to %s" % (radio, mode)
        else:
            return "Mode of %s is SSB" % radio

    @app.route("/status")
    def status():
        # Return switch status (Is this different from /config?  Is it necessary?)
        return "OK"

    @app.route("/switch/<port>", methods=["POST"])
    def switch(port):
        # Switch to <port>.
        return "Switch to port " + str(port)

    return app
