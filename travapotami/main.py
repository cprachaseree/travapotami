from flask import Blueprint, render_template

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def home():
    return render_template('./home.html')