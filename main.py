#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port = 3306,
                       user='root',
                       password='',
                       db='airsystem',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/check_flight')
def check_flight():
	return render_template('check_flight.html')
#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'

	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')
@app.route('/checkAuth', methods=['GET', 'POST'])
def checkAuth():
	source = request.form['source']
	destination = request.form['destination']
	return_date = request.form['return_date']
	departure = request.form['departure']
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'
	cursor.execute(query,(source,destination,departure))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	result = None
	if(data):
		#creates a session for the the user
		#session is a built in
		result = data
		return render_template('check_flight.html', result=result)
	else:
		#returns an error message to the html page
		error = 'such flight does not exist'
		return render_template('check_flight.html', error=error)
@app.route('/statusAuth', methods=['GET', 'POST'])
def statusAuth():
	airline = request.form['airline_name']
	flight_num = request.form['flight_number']
	return_date = request.form['return_date']
	departure = request.form['departure']
	cursor = conn.cursor()
	#executes query
	if departure:
		query = 'SELECT flight_status FROM flight WHERE airline_name = %s and flight_number = %s and departure_date_time = %s'
		cursor.execute(query,(airline,flight_num,departure))
	elif return_date:
		query = 'SELECT flight_status FROM flight WHERE airline_name = %s and flight_number = %s and arrival_date_time = %s'
		cursor.execute(query,(airline,flight_num,return_date))
	else:
		error = 'at least give one date please'
		return render_template('check_flight.html', error=error)

	#stores the results in a variable
	data2 = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error2 = None
	status = None
	if(data2):
		#creates a session for the the user
		#session is a built in
		status = data2
		return render_template('check_flight.html', status=status)
	else:
		#returns an error message to the html page
		error2 = 'such flight does not exist'
		return render_template('check_flight.html', error2=error2)
@app.route('/home')
def home():

    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


app.secret_key = 'some key that you will never guess'




#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 3000, debug = True)

