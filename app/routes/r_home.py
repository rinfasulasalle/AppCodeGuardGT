from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def get_home():
    return render_template('home/index.html')