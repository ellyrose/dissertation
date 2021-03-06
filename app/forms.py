from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,PasswordField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length,NoneOf,InputRequired, ValidationError
from wtforms.fields.html5 import DateField

COUNTRIES= [
    "United Kingdom",
    "Afghanistan",
    "Åland Islands",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia (Plurinational State of)",
    "Bonaire, Sint Eustatius and Saba",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "United States Minor Outlying Islands",
    "Virgin Islands (British)",
    "Virgin Islands (U.S.)",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cabo Verde",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo (Democratic Republic of the)",
    "Cook Islands",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Falkland Islands (Malvinas)",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Côte d'Ivoire",
    "Iran (Islamic Republic of)",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Macedonia (the former Yugoslav Republic of)",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia (Federated States of)",
    "Moldova (Republic of)",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Korea (Democratic People's Republic of)",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine, State of",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of Kosovo",
    "Réunion",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Martin (French part)",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten (Dutch part)",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "Korea (Republic of)",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Svalbard and Jan Mayen",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela (Bolivarian Republic of)",
    "Viet Nam",
    "Wallis and Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe"
]
# Create form classes to be used on html files 

class CreateAccountForm(FlaskForm):
    first_name= StringField("First Name", validators=[DataRequired(message="First name field is required"),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="First name")

    last_name= StringField("Last Name", validators=[DataRequired(message="Last name field is required"),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="Last name")

    birthdate= DateField("Birthdate", validators=[DataRequired(message="Birthdate field is required")])

    email_address= StringField("Email address", validators=[DataRequired(message="Email field is required"),
    Email(message="Your email address is not valid.")])

    country= SelectField("Country", validators=[DataRequired(message="Country field is required")], choices= COUNTRIES )

    password_hash = PasswordField('Password', validators=[DataRequired(message="Password field is required"),
    Length(min=12, max=30, message="Your password must contain at least 12 characters, and at most 30 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    

    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    accept_tos = BooleanField('I accept the Terms and Conditions', [validators.DataRequired()])

    submit= SubmitField("Submit")


class LoginForm(FlaskForm):
    email_address= StringField("Email address", validators=[DataRequired(),
    Email(message="Your email address is not valid.")])

    password_hash = PasswordField('Password', validators=[DataRequired()])

    submit= SubmitField("Submit")

class ForgottenPasswordForm(FlaskForm):
    email_address= StringField("Email address", validators=[DataRequired(),
    Email(message="Your email address is not valid.")])
   
    submit= SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField('Password', validators=[InputRequired(),
    Length(min=12, max=30, message="Your password must contain at least 12 characters, and at most 30 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    

    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    submit= SubmitField("Submit")

class LoggedInResetPasswordForm(FlaskForm):
    new_password = PasswordField('New password', validators=[
    Length(min=12, max=30, message="Your password must contain at least 12 characters, and at most 30 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    
    confirm = PasswordField('Repeat new password')
    password_hash = PasswordField('Please enter your current password to confirm any changes:', validators=[DataRequired()])
    submit= SubmitField("Submit")

class EditDetailsForm(FlaskForm):
    first_name= StringField("First Name", validators=[DataRequired()])
    last_name= StringField("Last Name", validators=[DataRequired()])
    birthdate= DateField("Birthdate",validators=[DataRequired()])
    email_address= StringField("Email address",validators=[DataRequired(),Email(message="Your email address is not valid.")])
    country=StringField("Country", validators=[DataRequired()])
    password_hash = PasswordField('Please enter your current password to confirm any changes:', validators=[DataRequired()])

    submit= SubmitField("Submit")



