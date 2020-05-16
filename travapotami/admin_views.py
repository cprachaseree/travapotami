'''
    ADMIN VIEWS MODULE: Module for admin related class  
    WHEN: Version 1 written 09-05-2020
    CALLING SEQUENCE: Is called when user tries to access admin page route /admin
    PURPOSE: This module contains MyModelView class which
             restricts who will be able to access the admin page.
'''
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

'''
    MODEL VIEWS CLASS: Class for restricting users who get to view admin
    CALLING SEQUENCE: This route is accessed when user access /admin route
    PURPOSE: To check if this user can access this admin page
    DATA STRUCTURES: Flask login module import
                     Flask admin model view 
    AlGORITHM: returns true if the user is logged in the user is web admin
'''
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_web_admin
