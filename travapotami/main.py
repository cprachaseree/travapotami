'''
    MAIN MODULE: Module for the main homepage route
    WHEN: Version 1 written 09-05-2020
    CALLING SEQUENCE: Is called when user tries to access home page /
    PURPOSE: This module contains homepage route with url '/'
'''
from flask import Blueprint, render_template

main_blueprint = Blueprint('main_blueprint', __name__)

'''
    HOME PAGE: Receives '/' route and renders home page
    CALLING SEQUENCE: This route is accessed when user enters the home page route
    PURPOSE: To be used when user goes to the home page
    AlGORITHM: if the route is '/', render the home page. 
'''
@main_blueprint.route('/')
def home():
    return render_template('./home.html')
