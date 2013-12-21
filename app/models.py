from app import db
from sqlalchemy import and_


class Travel(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	departure_place = db.Column(db.String(200), index = True)
	destination_place = db.Column(db.String(200), index = True)

	def __repr__(self):
		"""use for debugging, will print raw data."""
		return '<data %r>' %(self.departure_place)
	
	def search_travel(self, departure_place, destination_place):
		"""Search the record in the database which
		 	is equal to the user's input."""
	 	return Travel.query.filter(and_(Travel.departure_place.like \
										(departure_place), Travel. \
										destination_place.like( \
										destination_place))).first()
	
	def new_travel(self, departure_place, destination_place):
		"""Add new record of travel in the database."""
		new_travel = Travel(departure_place=departure_place, destination_place \
							=destination_place)
		db.session.add(new_travel)
		db.session.commit()


class Recommend(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), index = True)
	route_id = db.Column(db.Integer)

	def __init__(self, username, route_id):
		"""this will be the first method to run, when the class is called."""
		self.username = username
		self.route_id = route_id

	def __repr__(self):
		"""use for debugging, will print raw data."""
		return '<route_id: %r>' %(self.route_id)


class Route(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	instruction = db.Column(db.String(120), index = True)
	travel_id = db.Column(db.Integer)

	def __repr__(self):
		"""use for debugging, will print raw data."""
		return '<data %r>' %(self.instruction)
	
	def save_recommend(self, username):
		return Recommend(username, self.id)

	def vote_route(self, username, route_id):
		"""vote a route, save the username and
		 	route_id to filter who voted what."""
		vote = Recommend(username=username, route_id=route_id) 
 		db.session.add(vote)
 		db.session.commit()

	def new_route(self, instruction, travel_id):
		"""add a new route, save also the travel_id of the current searched 
			travel, use to know for what Travel that route is."""
		new_route = Route(instruction=instruction, travel_id=travel_id)
		db.session.add(new_route)
		db.session.commit()

	def routes_result(self, travel_id):
		return Travel.query.filter_by(travel_id = Travel.id).all()

	@property
	def votes(self):
	    return Recommend.query.filter_by(route_id = self.id).all()

	@property
	def count_votes(self):
		return len(self.votes)
	

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	pwd = db.Column(db.String(50), index = True) 

	# def __init__(self, username, email, pwd):
	# 	self.username = username
	# 	self.email = email
	# 	self.pwd = pwd
			
	def __repr__(self):
		"""use for debugging, will print raw data."""
		return '<data %r>' %(self.username)

	def authenticate_user(self, username, pwd):
		"""search if the user is registered in the database."""
	    	user = User.query.filter(and_(User.username==username,
	    	 							User.pwd==pwd)).first()
	    	if user:
	    		return True
	# def authenticate_user(self, username, pwd):
	# 	user = User.query.filter(and_(self.username==username, self.pwd==pwd)).first()
	# 	if user:
	# 		return True


	def validate_signup(self, username, email, pwd):
		"""register new user."""
	 	new_user = User(username=username, email=email, pwd=pwd)
 		if new_user:
 			return 
 		db.session.add(new_user)
 		db.session.commit()
		return True

	def invalid_username(self, username):
		"""search the database if the username is already taken"""
		username = User.query.filter_by(username=username).first()
		if username:
			return True

	def invalid_email(self, email):
		"""search the database if the email address is already used"""
		email = User.query.filter_by(email=email).first()
		if email:
			return True

	def invalid_username_email(self, username, email):
		"""search the database if the username and email is already taken"""
		email_username = User.query.filter(and_(User.username==username,
		 									User.email==email)).first()
		if email_username:
			return True

	def already_voted(self, username, route_id):
		"""search the database if the user already voted a route"""
		user_voted = Recommend.query.filter(and_(Recommend.username== \
													username, Recommend. \
													route_id==route_id)).first()
		if user_voted:
			return True