from flask import Flask, request, jsonify, current_app, session
from flask_jwt_extended import JWTManager

from datetime import datetime, timedelta, timezone

from Modules.API.Routes.routes import api
from App.Routes.routes import sites
from App.Helpers import helper as helper

def initialize_app():
    # get all required working directory
    working_dir = helper.get_curr_work_dir()

    # initialize flask application
    app = Flask(__name__, template_folder=working_dir['templates_dir'], static_url_path='', static_folder=working_dir['public_dir'])

    # initialize jwt
    jwt = JWTManager(app)

    # register blueprints
    app.register_blueprint(api)
    app.register_blueprint(sites)

    # initialize config
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # for deveopment only
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1) # for deveopment only
    app.config["JWT_SECRET_KEY"] = "super-secret-key" # for deveopment only

    app.secret_key = app.config["JWT_SECRET_KEY"] # for deveopment only

    return app, jwt

if __name__ == "__main__":
    app, jwt = initialize_app()
    app.run(host="0.0.0.0", debug=True)