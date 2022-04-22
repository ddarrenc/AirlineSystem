#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='project',
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

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Define route for customer login
@app.route('/customer_login')
def custlogin():
    return render_template('customerlogin.html')

#Define route for staff login
@app.route('/staff_login')
def stafflogin():
    return render_template('stafflogin.html')

#Define route for customer register 
@app.route('/customer_register')
def custregister():
    return render_template('customerregister.html')

#Define route for staff register
@app.route('/staff_register')
def staffregister():
    return render_template('staffregister.html')

# customer home
@app.route('/customerhome')
def cust_home():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name FROM customer WHERE customer_email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 
    cursor.close()
    firstname= data['first_name']
    lastname = data['last_name']
    return render_template('customerhome.html', username=username, firstname=firstname, lastname=lastname)

@app.route('/staffhome')
def staffhome():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name FROM airlinestaff WHERE user_name = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 
    cursor.close()
    firstname= data['first_name']
    lastname = data['last_name']
    return render_template('staffhome.html', username=username, firstname=firstname, lastname=lastname)

@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def custLoginAuth():
    #grabs information from the forms
    username = request.form.get('email')
    password = request.form.get('password')

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s and customer_password = %s'
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
        return redirect(url_for('cust_home'))
    else:
        #returns an error message to the html page
        error = 'Invalid username or password'
        return render_template('customerlogin.html', error=error)

@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
    #grabs information from the forms
    username = request.form.get('username')
    password = request.form.get('password')

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airlinestaff WHERE user_name = %s and staff_password = %s'
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
        return redirect(url_for('staffhome'))
    else:
        #returns an error message to the html page
        error = 'Invalid username or password'
        return render_template('stafflogin.html', error=error)

@app.route('/custRegisterAuth', methods=['GET', 'POST'])
def custRegisterAuth():
    #grabs information from the forms
    email     = request.form['email']
    password  = request.form['password']
    firstname = request.form['firstname']
    lastname  = request.form['lastname']
    buildnum  = request.form['buildnum']
    street    = request.form['street']
    city      = request.form['city']
    state     = request.form['state']

    passportnum     = request.form['passportnum']
    passportexpir   = request.form['passportexpir']
    passportcountry = request.form['passportcountry']

    dateofbirth = request.form['dateofbirth']
    phonenum = request.form['phonenum']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s'
    cursor.execute(query, (email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('customerregister.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, firstname, lastname, buildnum, street, city, state, 
                        passportnum, passportexpir, passportcountry, dateofbirth, phonenum))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
    #grabs information from the forms
    username  = request.form['username']
    password  = request.form['password']
    firstname = request.form['firstname']
    lastname  = request.form['lastname']
    airline   = request.form['airline']
    dateofbirth = request.form['dateofbirth']

    cursor = conn.cursor()
    query = 'SELECT * FROM airlinestaff WHERE user_name = %s AND airline_name = %s'
    cursor.execute(query, (username, airline))
    data = cursor.fetchone()
    error = None

    if(data):
        error = "This user already exists"
        return render_template('staffregister.html', error = error)
    else:
        query = 'SELECT * FROM airline WHERE airline_name = %s'
        cursor.execute(query, (airline))
        data = cursor.fetchone()

        if(not data):
            error = "The airline entered does not exist"
            return render_template('staffregister.html', error = error)
        else:
            ins = 'INSERT INTO airlinestaff (user_name, airline_name, staff_password, first_name, last_name, date_of_birth) VALUES(%s, (SELECT %s FROM airline), %s, %s, %s, %s)'
            cursor.execute(ins, (username, airline, password, firstname, lastname, dateofbirth))
            conn.commit()
            cursor.close()
            return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor()
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('cust_home'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
