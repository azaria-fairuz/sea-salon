from flask import Blueprint, render_template, jsonify

sites = Blueprint('sites', __name__)

@sites.route('/')
def index():
    return render_template('customers/index.html')