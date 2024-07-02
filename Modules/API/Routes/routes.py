import os, sys

from flask import Blueprint, jsonify, request, session
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

sys.path.append(os.getcwd())
from Modules.API.Controllers import ApiController as controller

# initialize bluprints
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def index():
    return jsonify(
        {
            'response': 'SEA-SALON is ready to accept requests!',
            'status': '200 OK',
            'messages': 'success'
        }
    )

@api.route("/register", methods=["POST"])
def register():
    try:
        response = 'Coming Soon!'
        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        response = controller.authenticate(data['user_email'], data['user_password'])

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        data = request.get_json()
        response = controller.remove_authentication(data['user_name'], data['access_token'], data['refresh_token'])

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        response = controller.refresh_token()
        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/reviews", methods=["GET", "POST"])
@jwt_required()
def reviews():
    try:
        if request.method == 'POST':
            data = request.get_json()
            response = controller.add_reviews(data['user_id'], data['service_id'], data['branch_id'], data['user_rating'], data['user_notes'])
        else:
            response = controller.get_reviews()

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )
    
@api.route("/branch", methods=["GET", "POST"])
@jwt_required()
def branch():
    try:
        if request.method == 'POST':
            response = 'Coming Soon!'
        else:
            response = controller.get_braches()

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/services", methods=["GET", "POST"])
@jwt_required()
def services():
    try:
        if request.method == 'POST':
            response = 'Coming Soon!'
        else:
            data = request.get_json()
            response = controller.get_services(data['branch_id'])

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )

@api.route("/reservation", methods=["GET", "POST"])
@jwt_required()
def reservation():
    try:
        if request.method == 'POST':
            data = request.get_json()
            response = controller.add_reservation(data['user_id'], data['phone'], data['service_id'], data['date'])
        else:
            if request.is_json:
                data = request.get_json()
                response = controller.get_reservation(data['user_id'])
            else:
                response = controller.get_reservation()

        return jsonify(
            {
                'response': response,
                'status': '200 OK',
                'messages': 'success'
            }
        )
    except Exception as e:
        return jsonify(
            {
                'response': str(e),
                'status': '200 OK',
                'messages': 'Something is Wrong!'
            }
        )