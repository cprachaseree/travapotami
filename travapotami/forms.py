from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, DecimalField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask import current_app, g
from flask.cli import with_appcontext
from flask_wtf.file import FileField, FileAllowed, FileRequired

countires = [('AF', 'AFGHANISTAN'),
            ('AL', 'ALBANIA'),
            ('DZ', 'ALGERIA'),
            ('AS', 'AMERICAN SAMOA'),
            ('AD', 'ANDORRA'),
            ('AO', 'ANGOLA'),
            ('AI', 'ANGUILLA'),
            ('AQ', 'ANTARCTICA'),
            ('AG', 'ANTIGUA AND BARBUDA'),
            ('AR', 'ARGENTINA'),
            ('AM', 'ARMENIA'),
            ('AW', 'ARUBA'),
            ('AU', 'AUSTRALIA'),
            ('AT', 'AUSTRIA'),
            ('AZ', 'AZERBAIJAN'),
            ('BS', 'BAHAMAS'), ('BH', 'BAHRAIN'),
            ('BD', 'BANGLADESH'),
            ('BB', 'BARBADOS'),
            ('BY', 'BELARUS'),
            ('BE', 'BELGIUM'),
            ('BZ', 'BELIZE'),
            ('BJ', 'BENIN'),
            ('BM', 'BERMUDA'),
            ('BT', 'BHUTAN'),
            ('BO', 'BOLIVIA'),
            ('BA', 'BOSNIA AND HERZEGOVINA'),
            ('BW', 'BOTSWANA'),
            ('BV', 'BOUVET ISLAND'),
            ('BR', 'BRAZIL'),
            ('IO', 'BRITISH INDIAN OCEAN TERRITORY'),
            ('BN', 'BRUNEI DARUSSALAM'),
            ('BG', 'BULGARIA'),
            ('BF', 'BURKINA FASO'),
            ('BI', 'BURUNDI'),
            ('KH', 'CAMBODIA'),
            ('CM', 'CAMEROON'),
            ('CA', 'CANADA'),
            ('CV', 'CAPE VERDE'),
            ('KY', 'CAYMAN ISLANDS'),
            ('CF', 'CENTRAL AFRICAN REPUBLIC'),
            ('TD', 'CHAD'),
            ('CL', 'CHILE'),
            ('CN', 'CHINA'),
            ('CX', 'CHRISTMAS ISLAND'),
            ('CC', 'COCOS (KEELING) ISLANDS'),
            ('CO', 'COLOMBIA'), ('KM', 'COMOROS'),
            ('CG', 'CONGO'),
            ('CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF'),
            ('CK', 'COOK ISLANDS'),
            ('CR', 'COSTA RICA'),
            ('HR', 'CROATIA'),
            ('CU', 'CUBA'),
            ('CY', 'CYPRUS'),
            ('CZ', 'CZECH REPUBLIC'),
            ('DK', 'DENMARK'),
            ('DJ', 'DJIBOUTI'),
            ('DM', 'DOMINICA'),
            ('DO', 'DOMINICAN REPUBLIC'),
            ('EC', 'ECUADOR'),
            ('EG', 'EGYPT'),
            ('SV', 'EL SALVADOR'),
            ('GQ', 'EQUATORIAL GUINEA'),
            ('ER', 'ERITREA'),
            ('EE', 'ESTONIA'),
            ('ET', 'ETHIOPIA'),
            ('FK', 'FALKLAND ISLANDS (MALVINAS)'),
            ('FO', 'FAROE ISLANDS'),
            ('FJ', 'FIJI'),
            ('FI', 'FINLAND'),
            ('FR', 'FRANCE'),
            ('GF', 'FRENCH GUIANA'),
            ('PF', 'FRENCH POLYNESIA'),
            ('TF', 'FRENCH SOUTHERN TERRITORIES'),
            ('GA', 'GABON'),
            ('GM', 'GAMBIA'),
            ('GE', 'GEORGIA'),
            ('DE', 'GERMANY'),
            ('GH', 'GHANA'),
            ('GI', 'GIBRALTAR'),
            ('GR', 'GREECE'),
            ('GL', 'GREENLAND'),
            ('GD', 'GRENADA'),
            ('GP', 'GUADELOUPE'),
            ('GU', 'GUAM'),
            ('GT', 'GUATEMALA'),
            ('GN', 'GUINEA'),
            ('GW', 'GUINEA'),
            ('GY', 'GUYANA'),
            ('HT', 'HAITI'),
            ('HM', 'HEARD ISLAND AND MCDONALD ISLANDS'),
            ('HN', 'HONDURAS'),
            ('HK', 'HONG KONG'),
            ('HU', 'HUNGARY'),
            ('IS', 'ICELAND'),
            ('IN', 'INDIA'),
            ('ID', 'INDONESIA'),
            ('IR', 'IRAN, ISLAMIC REPUBLIC OF'),
            ('IQ', 'IRAQ'),
            ('IE', 'IRELAND'),
            ('IL', 'ISRAEL'),
            ('IT', 'ITALY'),
            ('JM', 'JAMAICA'),
            ('JP', 'JAPAN'),
            ('JO', 'JORDAN'),
            ('KZ', 'KAZAKHSTAN'),
            ('KE', 'KENYA'),
            ('KI', 'KIRIBATI'),
            ('KP', "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF"),
            ('KR', 'KOREA, REPUBLIC OF'),
            ('KW', 'KUWAIT'),
            ('KG', 'KYRGYZSTAN'),
            ('LA', "LAO PEOPLE'S DEMOCRATIC REPUBLIC"),
            ('LV', 'LATVIA'),
            ('LB', 'LEBANON'),
            ('LS', 'LESOTHO'),
            ('LR', 'LIBERIA'),
            ('LY', 'LIBYAN ARAB JAMAHIRIYA'),
            ('LI', 'LIECHTENSTEIN'),
            ('LT', 'LITHUANIA'),
            ('LU', 'LUXEMBOURG'),
            ('MO', 'MACAO'),
            ('MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'),
            ('MG', 'MADAGASCAR'),
            ('MW', 'MALAWI'),
            ('MY', 'MALAYSIA'),
            ('MV', 'MALDIVES'),
            ('ML', 'MALI'),
            ('MT', 'MALTA'),
            ('MH', 'MARSHALL ISLANDS'),
            ('MQ', 'MARTINIQUE'),
            ('MR', 'MAURITANIA'),
            ('MU', 'MAURITIUS'),
            ('YT', 'MAYOTTE'),
            ('MX', 'MEXICO'),
            ('FM', 'MICRONESIA, FEDERATED STATES OF'),
            ('MD', 'MOLDOVA, REPUBLIC OF'),
            ('MC', 'MONACO'),
            ('MN', 'MONGOLIA'),
            ('MS', 'MONTSERRAT'),
            ('MA', 'MOROCCO'),
            ('MZ', 'MOZAMBIQUE'),
            ('MM', 'MYANMAR'),
            ('NA', 'NAMIBIA'),
            ('NR', 'NAURU'),
            ('NP', 'NEPAL'),
            ('NL', 'NETHERLANDS'),
            ('AN', 'NETHERLANDS ANTILLES'),
            ('NC', 'NEW CALEDONIA'),
            ('NZ', 'NEW ZEALAND'),
            ('NI', 'NICARAGUA'),
            ('NE', 'NIGER'),
            ('NG', 'NIGERIA'),
            ('NU', 'NIUE'),
            ('NF', 'NORFOLK ISLAND'),
            ('MP', 'NORTHERN MARIANA ISLANDS'),
            ('NO', 'NORWAY'),
            ('OM', 'OMAN'),
            ('PK', 'PAKISTAN'),
            ('PW', 'PALAU'),
            ('PS', 'PALESTINIAN TERRITORY, OCCUPIED'),
            ('PA', 'PANAMA'),
            ('PG', 'PAPUA NEW GUINEA'),
            ('PY', 'PARAGUAY'),
            ('PE', 'PERU'),
            ('PH', 'PHILIPPINES'),
            ('PN', 'PITCAIRN'),
            ('PL', 'POLAND'),
            ('PT', 'PORTUGAL'),
            ('PR', 'PUERTO RICO'),
            ('QA', 'QATAR'),
            ('RO', 'ROMANIA'),
            ('RU', 'RUSSIAN FEDERATION'),
            ('RW', 'RWANDA'),
            ('SH', 'SAINT HELENA'),
            ('KN', 'SAINT KITTS AND NEVIS'),
            ('LC', 'SAINT LUCIA'),
            ('PM', 'SAINT PIERRE AND MIQUELON'),
            ('VC', 'SAINT VINCENT AND THE GRENADINES'),
            ('WS', 'SAMOA'),
            ('SM', 'SAN MARINO'),
            ('ST', 'SAO TOME AND PRINCIPE'),
            ('SA', 'SAUDI ARABIA'),
            ('SN', 'SENEGAL'),
            ('CS', 'SERBIA AND MONTENEGRO'),
            ('SC', 'SEYCHELLES'),
            ('SL', 'SIERRA LEONE'),
            ('SG', 'SINGAPORE'),
            ('SK', 'SLOVAKIA'),
            ('SI', 'SLOVENIA'),
            ('SB', 'SOLOMON ISLANDS'),
            ('SO', 'SOMALIA'),
            ('ZA', 'SOUTH AFRICA'),
            ('GS', 'SOUTH GEORGIA AND SOUTH SANDWICH ISLANDS'),
            ('ES', 'SPAIN'),
            ('LK', 'SRI LANKA'),
            ('SD', 'SUDAN'),
            ('SR', 'SURINAME'),
            ('SJ', 'SVALBARD AND JAN MAYEN'),
            ('SZ', 'SWAZILAND'),
            ('SE', 'SWEDEN'),
            ('CH', 'SWITZERLAND'),
            ('SY', 'SYRIAN ARAB REPUBLIC'),
            ('TW', 'TAIWAN, PROVINCE OF CHINA'),
            ('TJ', 'TAJIKISTAN'),
            ('TZ', 'TANZANIA, UNITED REPUBLIC OF'),
            ('TH', 'THAILAND'),
            ('TL', 'TIMOR'),
            ('TG', 'TOGO'),
            ('TK', 'TOKELAU'),
            ('TO', 'TONGA'),
            ('TT', 'TRINIDAD AND TOBAGO'),
            ('TN', 'TUNISIA'),
            ('TR', 'TURKEY'),
            ('TM', 'TURKMENISTAN'),
            ('TC', 'TURKS AND CAICOS ISLANDS'),
            ('TV', 'TUVALU'),
            ('UG', 'UGANDA'),
            ('UA', 'UKRAINE'),
            ('AE', 'UNITED ARAB EMIRATES'),
            ('GB', 'UNITED KINGDOM'),
            ('US', 'UNITED STATES'),
            ('UM', 'UNITED STATES MINOR OUTLYING ISLANDS'),
            ('UY', 'URUGUAY'),
            ('UZ', 'UZBEKISTAN'),
            ('VU', 'VANUATU'),
            ('VN', 'VIET NAM'),
            ('VG', 'VIRGIN ISLANDS, BRITISH'),
            ('VI', 'VIRGIN ISLANDS, U.S.'),
            ('WF', 'WALLIS AND FUTUNA'),
            ('EH', 'WESTERN SAHARA'),
            ('YE', 'YEMEN'),
            ('ZW', 'ZIMBABWE')]

class TripForm(FlaskForm):

    tripname = StringField('Trip Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    destination = SelectField('Destination', choices=countires)
    description = TextAreaField('Description', validators=[DataRequired()])
    datebegin = DateField('Begin Date', format='%Y-%m-%d')
    dateend = DateField('End Date', format='%Y-%m-%d')
    min_budget = DecimalField('Minimum Budget', validators=[DataRequired(), NumberRange(min=0.0)])
    max_budget = DecimalField('Maximum Budget', validators=[DataRequired(), NumberRange(min=0.0)])
    triptype = StringField('Trip Name', validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('Create')


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

    passport_number = StringField('Passport number', validators=[DataRequired()])
    birthday = DateField('Date of Birth', format='%Y-%m-%d')
    photo = FileField('Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


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
        'Passport number', validators=[DataRequired()])
    birthday = DateField('Date of Birth', format='%Y-%m-%d')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')


class ForgotPasswordForm(FlaskForm):
<<<<<<< HEAD
       email = StringField('Email', validators=[DataRequired(), Email()])
       passport_number = StringField('Passport number', validators=[DataRequired()])
       submit = SubmitField('Request Change Password')

class NewPassword(FlaskForm):
       password = PasswordField('Password', validators=[DataRequired()])
       confirm_password = PasswordField('Confirm Password',
                                        validators=[DataRequired(), EqualTo('password')])  
       submit = SubmitField('Confirm New Password')
=======
    email = StringField('Email', validators=[DataRequired(), Email()])
    passport_no = StringField('Passport number', validators=[DataRequired()])
    submit = SubmitField('Confirm')

>>>>>>> 10abbb05c2413d036bbc2d485ad0861df2121a1c

class SearchUsersForm(FlaskForm):
    username = StringField('Search User by username', validators=[DataRequired()])
    submit = SubmitField('Search')


class UpdateImage(FlaskForm):
    photo = FileField('New Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Upload')


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

class SearchTrips(FlaskForm):
    pass
