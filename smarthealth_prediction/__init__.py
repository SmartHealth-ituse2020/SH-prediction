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

    @app.before_request
    def limit_remote_addr():
        if request.remote_addr != '127.0.0.1':  # != web app ip
            abort(403)  # Forbidden

    app.add_url_rule("/predict", view_func=predict.predict)
    return app

