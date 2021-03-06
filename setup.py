from setuptools import find_packages, setup

setup(
    name='travapotami',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'mysqlclient',
        'flask_bcrypt',
        'flask_login',
        'flask-admin',
        'flask_wtf',
        'flask_paginate',
        'pycountry'
    ],
)