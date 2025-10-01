from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class HotelForm(FlaskForm):
    h_name=StringField("Name", validators=[DataRequired()])
    ratings=StringField("Ratings",validators=[DataRequired()])
    service=StringField("Service",validators=[DataRequired()])
    map_url=StringField("Map url (optional)")
    submit = SubmitField("Add")