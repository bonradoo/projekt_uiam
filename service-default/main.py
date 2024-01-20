from flask import Flask, redirect, url_for

from blueprints.admin.admin import admin_bp
from blueprints.api.api import api_bp
from blueprints.user.user import user_bp
from blueprints.home.home import home_bp
from blueprints.login.login import login_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(login_bp, url_prefix='/login')

@app.route('/')
def index():
    return redirect(url_for('home.home'))

if __name__ == '__main__':
    app.run(debug=True)