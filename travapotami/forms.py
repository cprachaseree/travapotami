'''
    FORMS MODULE: Module that combine all form related modules
    CALLING SEQUENCE: Used to load or upload information to forms in specific routes
    WHEN: Version 1 written 09-05-2020
    PURPOSE: This module consists of classes that declare form types, inputs, and validations.
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, DecimalField, TextAreaField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask import current_app, g
from flask.cli import with_appcontext
from flask_wtf.file import FileField, FileAllowed, FileRequired

countires = [('AW', 'Aruba'), ('AF', 'Afghanistan'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AX', 'Åland Islands'), ('AL', 'Albania'), ('AD', 'Andorra'), ('AE', 'United Arab Emirates'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AS', 'American Samoa'), ('AQ', 'Antarctica'), ('TF', 'French Southern Territories'), ('AG', 'Antigua and Barbuda'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BI', 'Burundi'), ('BE', 'Belgium'), ('BJ', 'Benin'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BF', 'Burkina Faso'), ('BD', 'Bangladesh'), ('BG', 'Bulgaria'), ('BH', 'Bahrain'), ('BS', 'Bahamas'), ('BA', 'Bosnia and Herzegovina'), ('BL', 'Saint Barthélemy'), ('BY', 'Belarus'), ('BZ', 'Belize'), ('BM', 'Bermuda'), ('BO', 'Bolivia, Plurinational State of'), ('BR', 'Brazil'), ('BB', 'Barbados'), ('BN', 'Brunei Darussalam'), ('BT', 'Bhutan'), ('BV', 'Bouvet Island'), ('BW', 'Botswana'), ('CF', 'Central African Republic'), ('CA', 'Canada'), ('CC', 'Cocos (Keeling) Islands'), ('CH', 'Switzerland'), ('CL', 'Chile'), ('CN', 'China'), ('CI', "Côte d'Ivoire"), ('CM', 'Cameroon'), ('CD', 'Congo, The Democratic Republic of the'), ('CG', 'Congo'), ('CK', 'Cook Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CV', 'Cabo Verde'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('CW', 'Curaçao'), ('CX', 'Christmas Island'), ('KY', 'Cayman Islands'), ('CY', 'Cyprus'), ('CZ', 'Czechia'), ('DE', 'Germany'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DK', 'Denmark'), ('DO', 'Dominican Republic'), ('DZ', 'Algeria'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('ER', 'Eritrea'), ('EH', 'Western Sahara'), ('ES', 'Spain'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FI', 'Finland'), ('FJ', 'Fiji'), ('FK', 'Falkland Islands (Malvinas)'), ('FR', 'France'), ('FO', 'Faroe Islands'), ('FM', 'Micronesia, Federated States of'), ('GA', 'Gabon'), ('GB', 'United Kingdom'), ('GE', 'Georgia'), ('GG', 'Guernsey'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GN', 'Guinea'), ('GP', 'Guadeloupe'), ('GM', 'Gambia'), ('GW', 'Guinea-Bissau'), ('GQ', 'Equatorial Guinea'), ('GR', 'Greece'), ('GD', 'Grenada'), ('GL', 'Greenland'), ('GT', 'Guatemala'), ('GF', 'French Guiana'), ('GU', 'Guam'), ('GY', 'Guyana'), ('HK', 'Hong Kong'), ('HM', 'Heard Island and McDonald Islands'), ('HN', 'Honduras'), ('HR', 'Croatia'), ('HT', 'Haiti'), ('HU', 'Hungary'), ('ID', 'Indonesia'), ('IM', 'Isle of Man'), ('IN', 'India'), ('IO', 'British Indian Ocean Territory'), ('IE', 'Ireland'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IS', 'Iceland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('JP', 'Japan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KH', 'Cambodia'), ('KI', 'Kiribati'), ('KN', 'Saint Kitts and Nevis'), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LC', 'Saint Lucia'), ('LI', 'Liechtenstein'), ('LK', 'Sri Lanka'), ('LS', 'Lesotho'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('LV', 'Latvia'), ('MO', 'Macao'), ('MF', 'Saint Martin (French part)'), ('MA', 'Morocco'), ('MC', 'Monaco'), ('MD', 'Moldova, Republic of'), ('MG', 'Madagascar'), ('MV', 'Maldives'), ('MX', 'Mexico'), ('MH', 'Marshall Islands'), ('MK', 'North Macedonia'), ('ML', 'Mali'), ('MT', 'Malta'), ('MM', 'Myanmar'), ('ME', 'Montenegro'), ('MN', 'Mongolia'), ('MP', 'Northern Mariana Islands'), ('MZ', 'Mozambique'), ('MR', 'Mauritania'), ('MS', 'Montserrat'), ('MQ', 'Martinique'), ('MU', 'Mauritius'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('YT', 'Mayotte'), ('NA', 'Namibia'), ('NC', 'New Caledonia'), ('NE', 'Niger'), ('NF', 'Norfolk Island'), ('NG', 'Nigeria'), ('NI', 'Nicaragua'), ('NU', 'Niue'), ('NL', 'Netherlands'), ('NO', 'Norway'), ('NP', 'Nepal'), ('NR', 'Nauru'), ('NZ', 'New Zealand'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PA', 'Panama'), ('PN', 'Pitcairn'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PW', 'Palau'), ('PG', 'Papua New Guinea'), ('PL', 'Poland'), ('PR', 'Puerto Rico'), ('KP', "Korea, Democratic People's Republic of"), ('PT', 'Portugal'), ('PY', 'Paraguay'), ('PS', 'Palestine, State of'), ('PF', 'French Polynesia'), ('QA', 'Qatar'), ('RE', 'Réunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('SA', 'Saudi Arabia'), ('SD', 'Sudan'), ('SN', 'Senegal'), ('SG', 'Singapore'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('SJ', 'Svalbard and Jan Mayen'), ('SB', 'Solomon Islands'), ('SL', 'Sierra Leone'), ('SV', 'El Salvador'), ('SM', 'San Marino'), ('SO', 'Somalia'), ('PM', 'Saint Pierre and Miquelon'), ('RS', 'Serbia'), ('SS', 'South Sudan'), ('ST', 'Sao Tome and Principe'), ('SR', 'Suriname'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SE', 'Sweden'), ('SZ', 'Eswatini'), ('SX', 'Sint Maarten (Dutch part)'), ('SC', 'Seychelles'), ('SY', 'Syrian Arab Republic'), ('TC', 'Turks and Caicos Islands'), ('TD', 'Chad'), ('TG', 'Togo'), ('TH', 'Thailand'), ('TJ', 'Tajikistan'), ('TK', 'Tokelau'), ('TM', 'Turkmenistan'), ('TL', 'Timor-Leste'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TV', 'Tuvalu'), ('TW', 'Taiwan, Province of China'), ('TZ', 'Tanzania, United Republic of'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('US', 'United States'), ('UZ', 'Uzbekistan'), ('VA', 'Holy See (Vatican City State)'), ('VC', 'Saint Vincent and the Grenadines'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('VN', 'Viet Nam'), ('VU', 'Vanuatu'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('YE', 'Yemen'), ('ZA', 'South Africa'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]

trip_type = [('Relaxing', 'Relaxing'),
             ('Adventurous', 'Adventurous'),
             ('Foodies', 'Foodies'),
             ('Fast-paced', 'Fast-paced'),
             ('Slow-life', 'Slow-life')]
'''
    TRIPFORM: Form that needs to be filled out whenever the user is creating a new trip.
    CALLING SEQUENCE: Called on 'Create Trip' button after the trips tab is pressed.
    PURPOSE: Getting information from the user to design the trip.
    DATA STRUCTURES: SelectField with choices as a list of tuples, TextAreaFields for plain text
                    DateFields, DecimalField, SelectMultipleField with list of tuples as choices
                    and SubmitField.
    
'''

class TripForm(FlaskForm):

    destination = SelectField('Destination', choices=countires)
    description = TextAreaField('Description', validators=[DataRequired()])
    datebegin = DateField('Begin Date', format='%Y-%m-%d')
    dateend = DateField('End Date', format='%Y-%m-%d')
    max_budget = DecimalField('Maximum Budget (USD)', validators=[DataRequired(), NumberRange(min=0.0)])
    triptype = SelectMultipleField('Trip Types', choices=trip_type, validators=[DataRequired()])
    submit = SubmitField('Create')


'''
    REGISTRATIONFORM: Form that needs to be filled out whenever a new user wants to create an account.
    CALLING SEQUENCE: Called on 'Sign up' button.
    PURPOSE: Getting information from the user to create the new user and put it into the database.
    DATA STRUCTURES: SelectField with choices as a list of tuples, StringField for plain text
                    DateFields, PasswordField, FileField to upload the profile picture
                    and SubmitField.

'''

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])

    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Transmale', 'Transmale'),
                                            ('Transfemale', 'Transfemale'),
                                            ('Genderqueer', 'Genderqueer'),
                                            ('SomethingElse', 'Something else')])

    passport_number = StringField('Passport number', validators=[DataRequired(), Length(max=16)])
    birthday = DateField('Date of Birth', format='%Y-%m-%d')
    photo = FileField('Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Register')

'''
    LOGINFORM: Form that needs to be filled out whenever the user is logging in.
    CALLING SEQUENCE: Called on 'Login' button.
    PURPOSE: Getting information from the user to verify against information in the database.
    DATA STRUCTURES: StringField for plain text, PasswordField and SubmitField.
'''

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

'''
    UPDATEACCOUNTINFO: Form that needs to be filled out whenever the user wants to edit their account information.
    CALLING SEQUENCE: Called on 'Edit Account' button.
    PURPOSE: Getting information from the user to change their account information.
    DATA STRUCTURES: SelectField with choices as a list of tuples, StringField for plain text
                    DateFields, PasswordField, FileField to upload the profile picture
                    and SubmitField.
    ALGORITHM: If the user changes the information from any of the fields, these
                will be updated, however if the user does not change the information, they 
                will remain the same in the database.
'''
class UpdateAccountInfo(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])

    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Transmale', 'Transmale'),
                                            ('Transfemale', 'Transfemale'),
                                            ('Genderqueer', 'Genderqueer'),
                                            ('SomethingElse', 'Something else')])

    passport_number = StringField(
        'Passport number', validators=[DataRequired(), Length(max=16)])
    birthday = DateField('Date of Birth', format='%Y-%m-%d')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

'''
    FORGOTPASSWORDFORM: Form that needs to be filled out whenever the user forgets his or her password.
    CALLING SEQUENCE: Called on 'Forgot Password' button.
    PURPOSE: Authentication of the user to change password.
    DATA STRUCTURES: StringField for plain text and SubmitField.
    ALGORITHM: The user will need to input his or her passport number as well as the email
                in order to be able to change the password. 
'''
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    passport_number = StringField('Passport number', validators=[DataRequired()])
    submit = SubmitField('Request Change Password')

'''
    NEWPASSWORD: Form that needs to be filled out when updating the password
    CALLING SEQUENCE: Called after authentication of user when password is forgotten.
    PURPOSE: Updating password.
    DATA STRUCTURES: PasswordField and SubmitField.
'''

class NewPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirm New Password')

'''
    SEARCHUSERSFORM: Form that needs to be filled out when trying to find a user.
    CALLING SEQUENCE: Called on 'Find friends' button.
    PURPOSE: To find a user in order to see their profile.
    DATA STRUCTURES: String field for plain text and SubmitField.
'''
class SearchUsersForm(FlaskForm):
    username = StringField('Search User by username', validators=[DataRequired()])
    submit = SubmitField('Search')

'''
    UPDATEIMAGE: Form to change profile picture
    CALLING SEQUENCE: Called on 'Edit Account' button.
    PURPOSE: To change profile picture.
    DATA STRUCTURES: File field for jpg or png files and SubmitField.
'''
class UpdateImage(FlaskForm):
    photo = FileField('New Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Upload')

'''
    GIVERATINGS: Form that needs to be filled out whenever giving out rating to other users.
    CALLING SEQUENCE: Called on 'Rate this user' button.
    PURPOSE: To rate a user based on their friendliness, cleanliness, timeliness and foodies.
    DATA STRUCTURES: Select field with list of tuples as choices and SubmitField.
'''

class GiveRatings(FlaskForm):
    friendliness = SelectField('Friendliness', choices=[(1, 1.0),
                                                        (2, 2.0),
                                                        (3, 3.0),
                                                        (4, 4.0),
                                                        (5, 5.0)])
    cleanliness = SelectField('Cleanliness', choices=[(1, 1.0),
                                                      (2, 2.0),
                                                      (3, 3.0),
                                                      (4, 4.0),
                                                      (5, 5.0)])
    timeliness = SelectField('Timeliness', choices=[(1, 1.0),
                                                    (2, 2.0),
                                                    (3, 3.0),
                                                    (4, 4.0),
                                                    (5, 5.0)])
    foodies = SelectField('Foodies', choices=[(1, 1.0),
                                              (2, 2.0),
                                              (3, 3.0),
                                              (4, 4.0),
                                              (5, 5.0)])
    submit = SubmitField('Rate')

'''
    SEARCHTRIPFORM: Form that needs to be filled out when trying to find a user.
    CALLING SEQUENCE: Called on click of 'Join a trip' button.
    PURPOSE: To find a trip with based on differnet criteria such as destination, macimum budget or trip type.
    DATA STRUCTURES: SelectField and SelectMultipleField with list of tuples as choices, DecimalField and SubmitField.
'''

class SearchTripsForm(FlaskForm):
    destination = SelectField('Destination', choices=countires, validators=[DataRequired()])
    max_budget = DecimalField('Maximum Budget (USD) (Optional)', validators=[])
    triptype = SelectMultipleField('Trip Type (Optional)', choices=trip_type)
    submit = SubmitField('Search')


'''
    UPDATETRIP: Form that needs to be filled out whenever the host of a trip wants to edit information of the trip.
    CALLING SEQUENCE: Called on click of 'Edit trip' button.
    PURPOSE: To update any information of the trip that the user might want to change.
    DATA STRUCTURES: SelectField and SelectMultipleField with list of tuples as choices, DecimalField, TextAreaField
                    for plain text, DateField, and SubmitField.
    ALGORITHM:If the user changes the information from any of the fields, these
                will be updated, however if the user does not change the information, they 
                will remain the same in the database.
'''

class UpdateTrip(FlaskForm):
    destination = SelectField('Destination', choices=countires)
    # participants = StringField('Add Participants Usernames (separated by \',\' ex. User1,User2)')
    # participantsremoved = StringField('Remove Participants Usernames (separated by \',\' ex. User1,User2)')
    description = TextAreaField('Description')
    datebegin = DateField('Begin Date', format='%Y-%m-%d')
    dateend = DateField('End Date', format='%Y-%m-%d')
    max_budget = DecimalField('Maximum Budget (USD)', validators=[NumberRange(min=0.0)])
    triptype = SelectMultipleField('Trip Types', choices=trip_type)
    submit = SubmitField('Update')

'''
    ADDHOSTPARTICIPANT: Form that needs to be filled out after updating trip, in case the host wants to add
                    another host or participant.
    CALLING SEQUENCE: Called on click of 'Add' (hosts or participants) button.
    PURPOSE: To add a new host or participant to a trip.
    DATA STRUCTURES: StringField for plain text and SubmitField.
    
'''
class AddHostParticipant(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add')
