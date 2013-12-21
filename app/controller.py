# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, request, session, jsonify
from app import app, db, models 
from forms import SearchForm, LoginForm, SignUpForm, AddRouteForm
from models import User, Travel, Route, Recommend
from sqlalchemy import and_, desc

#newly added
# @app.route('/travels', methods=['GET', 'POST'])
# def travels():
# 	travels = Travel.query.all()
# 	routes = Route.query.filter_by(travel_id=travels.id).count()
# 	routes =  sorted(travels, key = lambda route: -routes)
# 	return render_template('travels.html', routes=routes)


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
	"""index/search page, will get data from the templates then pass it to 
	bestroute to validate if the searched data is registered in the database 
	return errors if textfields are not supplied care of the form object"""
	form = SearchForm()

	if 'username' in session:
		username = session['username']
	else:
		username = ''

	if form.validate_on_submit():
		session['start'] = form.departure_place.data
		session['end'] = form.destination_place.data		
		return redirect('/bestroute')
	return render_template('index.html', form=form, username = username)


@app.route('/bestroute', methods=['GET', 'POST'])
def bestroute():
	"""first check the session from the searched data, if empty redirect to 
	the index page.Check if the searched data is in the database, sort the data
	into their number of votes(desc order), if the data is not registered in
	the database, will redirect to suggestAddTravel to give the user the option
	to add the searched data in the database. return all the data gathered and 
	pass it to the template."""
	if 'start' not in session:
		return	redirect('/index')

	form = AddRouteForm()
	travel = Travel().search_travel(session['start'], session['end'])
	
	if travel is None:
			return render_template('suggestAddTravel.html', departure=session \
									['start'], destination=session['end'])
	
	travel_id = travel.id
	routes = models.Route.query.filter_by(travel_id = travel_id).order_by( \
											Route.id.desc()).all()
	#sort the routes(which is iterable), 
	routes =  sorted(routes, key = lambda route: -route.count_votes)
	if 'username' in session:
		username = session['username']
	else:
		username = ''

	if form.validate_on_submit():
		Route().new_route(form.suggested_route.data, travel_id)
		return redirect('/bestroute')	
	return render_template('bestroute.html', travel=travel, username=username, \
							 routes=routes, form=form, departure= \
							 session['start'], destination=session['end'])


@app.route('/addTravel', methods=['GET', 'POST'])
def addTravel():
	"""Will add the searched data to the database, and redirect to the 
	bestroute page."""
	travel = Travel()
	travel.new_travel(session['start'], session['end'])
	return redirect('/bestroute')


@app.route('/recommend/<route_id>', methods=['GET', 'POST'])
def recommend(route_id):
	"""vote any routes, but first check if the user is logged in, if not 
	redirect to the login page, and if the user already voted a specific route
	an error message will that he/she already voted."""
	route_id = route_id
	user = User()
	route = Route()
	if 'username' in session:
		if user.already_voted(session['username'], route_id):
			flash('You already voted that route.')
			return redirect('/bestroute')
		route.vote_route(session['username'], route_id)
		return redirect('/bestroute')
	else:
		return redirect('/login')	


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	"""Register new user to the database, but first will check if the entered 
	data is already in the database."""
	form = SignUpForm()
	new_user = User()
	error=''
	if form.validate_on_submit():
		if new_user.invalid_username(form.username.data):
			error = 'username already exist'
		elif new_user.invalid_email(form.email.data):
			error = 'email already exist'
		elif new_user.invalid_username_email(form.username.data, form.email.data):
			error = 'username and email already exist'				
		else: 
			new_user.validate_signup(form.username.data, form.email.data,
									form.pwd.data)
			session['username'] = form.username.data
			return redirect('/bestroute')
	return render_template('signup.html', form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""logged in the user, and will check if the user is registered in the 
	database, if not will an error message."""
	form = LoginForm()
	user = User()
	if form.validate_on_submit():
		if 'start' not in session:
			session['username'] = form.username.data
			return redirect('/index')
		elif user.authenticate_user(form.username.data, form.pwd.data):
			session['username'] = form.username.data
			return redirect('/bestroute')
		else:
			error = 'Username/Password did not match.'
			return render_template('login.html', form=form, error=error)
	return render_template('login.html', form=form)
	

@app.route('/logout')
def logout():
	"""log out the user and will clear the sessions."""
	session.pop('username', None)
	session.pop('start', None)
	session.pop('end', None)
	return redirect('/index') 