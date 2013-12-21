from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(Form):
	departure_place = TextField('departure_place', validators = [DataRequired()])
	destination_place = TextField('destination_place', validators = [DataRequired()])

class SignUpForm(Form):
	username = TextField('username', validators = [DataRequired()])
	email = TextField('email', validators = [DataRequired()])
	pwd = TextField('pwd', validators = [DataRequired()])

class LoginForm(Form):
	username = TextField('username', validators = [DataRequired()])
	pwd = TextField('pwd', validators = [DataRequired()])

class AddRouteForm(Form):
	suggested_route = TextAreaField('suggested_route', validators = [DataRequired()])