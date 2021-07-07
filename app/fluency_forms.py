from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,IntegerField,HiddenField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length,NoneOf,InputRequired, ValidationError
from wtforms.fields.html5 import DateField

DAYS= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DATE=range(1,32)
MONTH= ["January","February","March","April","May","June","July","August","September","October","November","December"]
YEAR= range(1950,2051)
SEASON= ["Spring","Summer", "Autumn","Winter"]
OPTIONS= range(1,13)
AGE= range(1,100)
AREAS= ["Fluency Fountain", "Memory Maze", "Language Lake", "Visual Veg-Plot"]
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

class Fluency_1(FlaskForm):
    tries = HiddenField("tries")
    day= SelectField(label="What day is it?", validators=[DataRequired()], choices=DAYS)
    date= SelectField(label="What is the date?", validators=[DataRequired()], choices=DATE)
    month= SelectField(label="What month are we in?", validators=[DataRequired()], choices=MONTH)
    year= SelectField(label="What year is it?", validators=[DataRequired()], choices=YEAR)
    season= SelectField(label="What season are we in?", validators=[DataRequired()], choices=SEASON)
    birthdate= DateField("What is your date of birth?", validators=[DataRequired()])
    email_address= StringField("What is your email address?", validators=[DataRequired()])
    test_place= SelectField("Which area of the test are you in?", validators=[DataRequired()], choices=AREAS)
    age= SelectField(label="How old are you?", validators=[DataRequired()], choices=AGE)
    country= StringField("Which country do you live in?", validators=[DataRequired()], choices= COUNTRIES)
    
    submit= SubmitField("Submit")

class Fluency_2(FlaskForm):
    v1= StringField(label="Name of item 1:", validators=[DataRequired()])
    v2= StringField(label="Name of item 2:", validators=[DataRequired()])
    v3= StringField(label="Name of item 3:", validators=[DataRequired()])

    submit= SubmitField("Submit")

class Fluency_3(FlaskForm):
    v1= IntegerField(label="Answer 1", validators=[DataRequired()])
    v2= IntegerField(label="Answer 2", validators=[DataRequired()])
    v3= IntegerField(label="Answer 3", validators=[DataRequired()])
    v4= IntegerField(label="Answer 4", validators=[DataRequired()])
    v5= IntegerField(label="Answer 5", validators=[DataRequired()])

    submit= SubmitField("Submit")

class Fluency_4(FlaskForm):
    

    submit= SubmitField("Submit")

class Fluency_5(FlaskForm):
    v1= StringField(label="What is the name of the current Prime Minister?", validators=[DataRequired()])
    v2= StringField(label="Name the first woman who was Prime Minister:", validators=[DataRequired()])
    v3= StringField(label="Name the USA President:", validators=[DataRequired()])
    v4= StringField(label="What is the name of the USA President who was assassinated in the 1960s?", validators=[DataRequired()])
   
    submit= SubmitField("Submit")

class Fluency_6(FlaskForm):

    submit= SubmitField("Submit")


class Fluency_7(FlaskForm):
    v1= StringField(label="Name of item 1:", validators=[DataRequired()])
    v2= StringField(label="Name of item 2:", validators=[DataRequired()])
    v3= StringField(label="Name of item 3:", validators=[DataRequired()])
    v4= StringField(label="Name of item 4:", validators=[DataRequired()])
    v5= StringField(label="Name of item 5:", validators=[DataRequired()])
    v6= StringField(label="Name of item 6:", validators=[DataRequired()])
    v7= StringField(label="Name of item 7:", validators=[DataRequired()])
    v8= StringField(label="Name of item 8:", validators=[DataRequired()])
    v9= StringField(label="Name of item 9:", validators=[DataRequired()])
    v10= StringField(label="Name of item 10:", validators=[DataRequired()])
    v11= StringField(label="Name of item 11:", validators=[DataRequired()])
    v12= StringField(label="Name of item 12:", validators=[DataRequired()])

    submit= SubmitField("Submit")

class Fluency_8(FlaskForm):
    v1= SelectField(label="Which item is associated with the monarchy?", validators=[DataRequired()], choices=OPTIONS)
    v2= SelectField(label="Which item is a marcupial?", validators=[DataRequired()], choices=OPTIONS)
    v3= SelectField(label="Which item can be found in the Antartic?", validators=[DataRequired()], choices=OPTIONS)
    v4= SelectField(label="Which item has a nautical connection?", validators=[DataRequired()], choices=OPTIONS)
   
    submit= SubmitField("Submit")


class Fluency_9(FlaskForm):
    v1= IntegerField(label="Number of dots in image 1", validators=[DataRequired()])
    v2= IntegerField(label="Number of dots in image 2", validators=[DataRequired()])
    v3= IntegerField(label="Number of dots in image 3", validators=[DataRequired()])
    v4= IntegerField(label="Number of dots in image 4", validators=[DataRequired()])

    submit= SubmitField("Submit")

class Fluency_10(FlaskForm):
    v1= StringField(label="Letter in image 1", validators=[DataRequired()])
    v2= StringField(label="Letter in image 2", validators=[DataRequired()])
    v3= StringField(label="Letter in image 3", validators=[DataRequired()])
    v4= StringField(label="Letter in image 4", validators=[DataRequired()])

    submit= SubmitField("Submit")