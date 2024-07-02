from flask import Blueprint, render_template, jsonify

sites = Blueprint('sites', __name__)

@sites.route('/')
def index():
    return jsonify(
        {
            'response': 'SEA SALON is ready to be accessed',
            'status': '200 OK',
            'messages': 'success'
        }
    )