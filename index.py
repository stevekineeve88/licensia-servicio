from flask import Flask
from modules.license.controllers.api.v1.status_controller import license_status_v1_api

app = Flask(__name__)

app.register_blueprint(license_status_v1_api)


@app.route("/", methods=["GET"])
def health_check():
    """ GET healthcheck
    Returns:
        tuple
    """
    return {
        "test": "hello world"
    }, 200
