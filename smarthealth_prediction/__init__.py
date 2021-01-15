from flask import Flask, abort, request, Response
from smarthealth_prediction import predict
from decouple import config


def create_app(cfg="DEV"):

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    if cfg == "TESTING":
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    ALLOWED_DOMAINS = [
        "52.214.149.142",
        "54.77.113.178",
        "52.50.35.172",
        "34.252.129.97",
        "34.251.140.205",
        "52.50.189.174",
        "52.213.192.18",
        "34.250.41.57",
    ]
    @app.before_request
    def limit_remote_addr():
        if request.remote_addr not in ALLOWED_DOMAINS:  # != web app ip
            abort(403)  # Forbidden

    app.add_url_rule("/predict", view_func=predict.predict)
    return app
