from flask import Blueprint, render_template, redirect, url_for

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_bp.route('/', methods=['GET'])
def admin():
    return render_template('user.html')