from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
import os

from switchapi.BB import BB
from switchapi.Transverter import Transverter

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('switchapi.config.BaseConfig')

    basic_auth = BasicAuth(app)

    beaglebone = BB(xverters=[Transverter("SG Labs 33cm", "902"),
                              Transverter("SG Labs 23cm", "1296", isDefault=True),
                              Transverter("SG Labs 13cm", "2304"),
                              None, None, None, None, None])
    beaglebone.initHW()

    @app.route("/active")
    def active():
        # Return the currently active band.
        retval = beaglebone.activeBand
        if not retval:
            return jsonify({"active": "Nothing"}), 200

        return jsonify({"active": retval}), 200

    # @app.route("/config")
    # def config():
    #     # Return the complete configuration of the switch
    #     return jsonify({}), 200

    @app.route("/config/bands")
    @basic_auth.required
    def config_bands():
        # Return just the supported bands
        return jsonify({"bands": beaglebone.bands}), 200

    @app.route("/switch/<band>")
    @basic_auth.required
    def switch(band):
        # Switch to <band>.
        try:
            beaglebone.activateBand(band)
        except ValueError as e:
            return jsonify({"switch": band, "result": "failure",
                            "reason": str(e)}), 400
        else:
            return jsonify({"switch": band, "result": "success"}), 200

    return app

app = create_app()
