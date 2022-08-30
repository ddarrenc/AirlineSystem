'''
Darren Chan (dc4261)
Sicheng Xie (sx810)

Airline Reservation System
'''

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from numpy import average
from datetime import datetime
from platformdirs import user_cache_dir
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
    username = session.get('username')

    if not username:
        return render_template('index.html')
    else:
        cursor = conn.cursor()
        query = 'SELECT * FROM customer WHERE customer_email = %s'
        cursor.execute(query, (username))

        custdata = cursor.fetchone()

        if not custdata:
            query = 'SELECT * FROM airlinestaff WHERE user_name = %s'
            cursor.execute(query, (username))
            staffdata = cursor.fetchone()

            if not staffdata:
                return render_template('index.html')
            else:
                cursor.close()
                return staffhome()
        else:
            cursor.close()
            return cust_home()


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


@app.route('/check_flight')
def check_flight():
	return render_template('check_flight.html')


@app.route('/staff_flight_search')
def staff_flight_search():
    return render_template('staff_flight_search.html')


@app.route('/staff_flight_create')
def staff_flight_create():
    return render_template('staff_flight_create.html')


@app.route('/staff_change_status')
def staff_status_change():
    return render_template('staff_change_status.html')


@app.route('/staff_airport_create')
def staff_airport_create():
    return render_template('staff_airport_create.html')


@app.route('/staff_rating_view')
def staff_rating_view():
    return render_template('staff_rating_view.html')


@app.route('/checkspending')
def checkspending():
    return render_template('checkspending.html')


@app.route('/checkandbook')
def checkandbook():
    return render_template('checkandbook.html')


@app.route('/checkcancelandcomment')
def checkcancelandcomment():
    return render_template('checkcancelandcomment.html')


@app.route('/check_flight')
def flight_checker_register():
    return render_template('/check_flight.html')

@app.route('/staff_addphone')
def staff_addphone():
    return render_template('/staff_addphone.html')

@app.route('/staff_frequentcust_view')
def staff_frequentcust_view():
    # Check if logged in
    username = session.get('username')
    if not username:
        return redirect('/')

    # Authenticate Staff Query
    cursor = conn.cursor()
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # Failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_frequentcust_view.html', error = error)
    
    airline_name = authdata['airline_name']

    query = 'SELECT customer_email, COUNT(*) as numCount FROM ticket WHERE airline_name = %s AND '\
        'purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR) AND ' \
        'purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) GROUP BY customer_email ORDER BY numCount DESC LIMIT 3'

    cursor.execute(query, (airline_name))
    most_frequent_customers = cursor.fetchall()
    cursor.close()

    if len(most_frequent_customers) == 0:
        none_frequent = 'No frequent customers within the last year...'
        return render_template('staff_frequentcust_view.html', none_frequent = none_frequent)

    return render_template('staff_frequentcust_view.html', most_frequent_customers = most_frequent_customers)


@app.route('/staff_reports_view')
def staff_reports_view():
    return render_template('staff_reports_view.html')


@app.route('/staff_revenue_view')
def staff_revenue_view():
    # Check if logged in
    username = session.get('username')
    if not username:
        return redirect('/')

    # Authenticate Staff Query
    cursor = conn.cursor()
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # Failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_frequentcust_view.html', error = error)
    
    airline_name = authdata['airline_name']

    # Yearly revenue 
    year_revenue_query = 'SELECT airline_name, SUM(sold_price) as year_revenue FROM ticket WHERE airline_name = %s AND ' \
        'purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR) AND ' \
            'purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) GROUP BY airline_name'

    cursor.execute(year_revenue_query, (airline_name))
    year_revenue = cursor.fetchone()

    if year_revenue == None:
        year_revenue = '0'
    else:
        year_revenue = year_revenue['year_revenue']

    # Monthly revenue
    month_revenue_query = 'SELECT airline_name, SUM(sold_price) as month_revenue FROM ticket WHERE airline_name = %s AND ' \
        'purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH) AND ' \
            'purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) GROUP BY airline_name'

    cursor.execute(month_revenue_query, (airline_name))
    month_revenue = cursor.fetchone()

    if month_revenue == None:
        month_revenue = '0'
    else:
        month_revenue = month_revenue['month_revenue']

    # First Class Revenue 
    class_revenue_query = 'SELECT airline_name, SUM(sold_price) as class_revenue FROM ticket ' \
        ' WHERE airline_name = %s AND travel_class = %s GROUP BY airline_name'

    cursor.execute(class_revenue_query, (airline_name, 'First'))
    first_class_revenue = cursor.fetchone()

    if first_class_revenue == None:
        first_class_revenue = '0'
    else:
        first_class_revenue = first_class_revenue['class_revenue']

    # Business Class Revenue
    cursor.execute(class_revenue_query, (airline_name, 'Business'))
    business_class_revenue = cursor.fetchone()

    if business_class_revenue == None:
        business_class_revenue = '0'
    else:
        business_class_revenue = business_class_revenue['class_revenue']

    # Economy Class Revenue
    cursor.execute(class_revenue_query, (airline_name, 'Economy'))
    economy_class_revenue = cursor.fetchone()

    if economy_class_revenue == None:
        economy_class_revenue = '0'
    else:
        economy_class_revenue = economy_class_revenue['class_revenue']
    
    # Top 3 most popular destinations from last year
    query = 'SELECT T.arrival_airport_code, COUNT(*) as num FROM (ticket NATURAL JOIN flight as T) ' \
        'JOIN airport A ON T.arrival_airport_code = A.airport_code WHERE airline_name = %s ' \
        'AND purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR) AND purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) ' \
        'GROUP BY airline_name, T.arrival_airport_code ' \
        'ORDER BY num DESC LIMIT 3'

    cursor.execute(query, (airline_name))
    toplastyear = cursor.fetchall()

    # Top 3 most poopular from last 3 months
    query = 'SELECT T.arrival_airport_code, COUNT(*) as num FROM (ticket NATURAL JOIN flight as T) ' \
        'JOIN airport A ON T.arrival_airport_code = A.airport_code WHERE airline_name = %s ' \
        'AND purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 3 MONTH) AND purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) ' \
        'GROUP BY airline_name, T.arrival_airport_code ' \
        'ORDER BY num DESC LIMIT 3'

    cursor.execute(query, (airline_name))
    toplastmonths = cursor.fetchall()

    return render_template('staff_revenue_view.html', 
        year_revenue = year_revenue, 
        month_revenue = month_revenue,
        first_class_revenue = first_class_revenue,
        business_class_revenue = business_class_revenue,
        economy_class_revenue = economy_class_revenue,
        toplastyear = toplastyear,
        toplastmonths = toplastmonths)


@app.route('/staff_plane_create')
def staff_plane_create():
    error = None
    cursor = conn.cursor()
    username = session.get('username')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return redirect(url_for('hello'))
       # return render_template('staff_plane_create.html', error=error)
    
    airline_name = authdata['airline_name']
    
    query = 'SELECT * FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    ownedPlanes = cursor.fetchall()
    cursor.close()

    return render_template('staff_plane_create.html', ownedPlanes = ownedPlanes)


# customer home
@app.route('/customerhome')
def cust_home():
    try:
        username = session['username']
    except:
        return redirect('/')
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
    try:
        username = session['username']
    except:
        return redirect('/')
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name, airline_name FROM airlinestaff WHERE user_name = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 

    if not data:
        return redirect(url_for('hello'))

    firstname= data['first_name']
    lastname = data['last_name']
    airline_name = data['airline_name']

    query = 'SELECT * FROM `flight` WHERE departure_date_time <= CURRENT_DATE + INTERVAL 30 DAY AND departure_date_time >= NOW() AND airline_name = %s;'
    cursor.execute(query, (airline_name))
    cursor.close()
    flightdata = cursor.fetchall() 
    
    return render_template('staffhome.html', username=username, firstname=firstname, lastname=lastname, upcomingstatus=flightdata)


@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def custLoginAuth():
    #grabs information from the forms
    username = request.form.get('email')
    password = request.form.get('password')

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s and customer_password = MD5(%s)'
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
    query = 'SELECT * FROM airlinestaff WHERE user_name = %s and staff_password = MD5(%s)'
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
        session['staff_airline'] = data['airline_name']
        return redirect(url_for('staffhome'))
    else:
        #returns an error message to the html page
        error = 'Invalid username or password'
        return render_template('stafflogin.html', error=error)
'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'


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
    phonenum = request.form['phone_number']

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
        ins = 'INSERT INTO customer VALUES(%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, firstname, lastname, buildnum, street, city, state, 
                        passportnum, passportexpir, passportcountry, dateofbirth, phonenum))
        conn.commit()
        cursor.close()

        success = 'New customer successfully registered!'
        return render_template('index.html', success=success)


@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
    #grabs information from the forms
    username  = request.form['username']
    password  = request.form['password']
    firstname = request.form['firstname']
    lastname  = request.form['lastname']
    airline   = request.form['airline']
    dateofbirth = request.form['dateofbirth']
    phone_number = request.form['phone_number']

    cursor = conn.cursor()
    query = 'SELECT * FROM airlinestaff WHERE user_name = %s AND airline_name = %s'
    cursor.execute(query, (username, airline))
    data = cursor.fetchone()
    error = None

    if(data):
        error = "User already exists!"
        return render_template('staffregister.html', error = error)
    else:
        query = 'SELECT * FROM airline WHERE airline_name = %s'
        cursor.execute(query, (airline))
        data = cursor.fetchone()

        if(not data):
            error = "The airline entered does not exist!"
            return render_template('staffregister.html', error = error)
        else:
            ins = 'INSERT INTO airlinestaff (user_name, airline_name, staff_password, first_name, last_name, date_of_birth) VALUES(%s, (SELECT * FROM airline WHERE airline_name = %s), MD5(%s), %s, %s, %s)'
            cursor.execute(ins, (username, airline, password, firstname, lastname, dateofbirth))
            conn.commit()
            
            if phone_number:
                insPhone = 'INSERT INTO phonenumber VALUES ((SELECT user_name FROM airlinestaff WHERE user_name = %s), %s)'
                cursor.execute(insPhone, (username, phone_number))
                conn.commit()

            cursor.close()
            success = 'New staff member registered!'
            return render_template('index.html', success = success)


@app.route('/checkAuth', methods=['GET', 'POST'])
def checkAuth():
    source = request.form['source']
    destination = request.form['destination']
    return_date = request.form['return_date']
    departure = request.form['departure']
    now = datetime.now()
    time = now.strftime("%Y-%m-%d")
    if time > departure:
        error = "You can't book past flights"
        return render_template('check_flight.html', error=error)
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'
    cursor.execute(query, (source, destination, departure))
    # stores the results in a variable
    data1 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    cursor = conn.cursor()
    result2 = None
    data2 = None
    print(time > departure)
    if return_date:
        if return_date < departure:
            error = "not valid time range"
            return render_template('check_flight.html', error=error)
        else:
            query = 'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'
            cursor.execute(query, (destination, source, return_date))
            data2 = cursor.fetchall()
            cursor.close()
    result = []
    result2 = []
    if (data1):
        for i in data1:
            result.append(
                "airline: " + i["airline_name"] + " ; flight number: " + i["flight_number"] + " ; depart time: " + i[
                    "departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S"))
        # creates a session for the the user
        # session is a built in
        if (data2):
            for i in data2:
                result2.append(
                    "airline: " + i["airline_name"] + " ; flight number: " + i["flight_number"] + " ; depart time: " +
                    i["departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S"))
            return render_template('check_flight.html', result=result, result2=result2)
        else:
            for i in data1:
                result.append(
                    "airline: " + i["airline_name"] + " ; flight number: " + i["flight_number"] + " ; depart time: " +
                    i["departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S"))
            if return_date:
                result2 = "we currently do not have return flight for you"
                return render_template('check_flight.html', result=result, result2=result2)
            else:
                return render_template('check_flight.html', result=result)
    else:
        # returns an error message to the html page
        error = 'such flight does not exist'
        return render_template('check_flight.html', error=error)


@app.route('/statusAuth', methods=['GET', 'POST'])
def statusAuth():
    airline = request.form['airline_name']
    flight_num = request.form['flight_number']
    return_date = request.form['return_date']
    departure = request.form['departure']
    cursor = conn.cursor()
    # executes query
    if departure:
        query = 'SELECT flight_status FROM flight WHERE airline_name = %s and flight_number = %s and departure_date_time = %s'
        cursor.execute(query, (airline, flight_num, departure))
    elif return_date:
        query = 'SELECT flight_status FROM flight WHERE airline_name = %s and flight_number = %s and arrival_date_time = %s'
        cursor.execute(query, (airline, flight_num, return_date))
    else:
        error = 'at least give one date please'
        return render_template('check_flight.html', error=error)

    # stores the results in a variable
    data2 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error2 = None
    status = None
    if (data2):
        # creates a session for the the user
        # session is a built in
        status = data2
        return render_template('check_flight.html', status=status)
    else:
        # returns an error message to the html page
        error2 = 'such flight does not exist'
        return render_template('check_flight.html', error2=error2)


@app.route('/staff_search_auth', methods=['GET', 'POST'])
def staff_search_auth():
    airline_name = request.form['airline_name']
    flightNum = request.form['flightNum']
    departureDate  = request.form['departureDate']
    arrivalDate = request.form['arrivalDate']
    departureCode = request.form['departureCode']
    arrivalCode  = request.form['arrivalCode']
    basePrice   = request.form['basePrice']
    flightStatus = request.form['flightStatus']
    planeID = request.form['planeID']

    error = None
    cursor = conn.cursor()
    username = session.get('username')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_flight_search.html', error = error)

    query = 'SELECT * FROM flight WHERE '

    if airline_name:
        query += ' airline_name = \'%s\'' % (airline_name)
    
    if flightNum:
        query += ' AND flight_number = \'%s\'' % (flightNum)
    
    if departureDate:
        query += ' AND departure_date_time >= \'%s\'' % (departureDate)
    
    if departureCode:
        query += ' AND departure_airport_code = \'%s\'' % (departureCode)

    if arrivalCode:
        query += ' AND arrival_airport_code = \'%s\'' % (arrivalCode)

    if arrivalDate:
        query += ' AND arrival_date_time <= \'%s\'' % (arrivalDate)

    if flightStatus:
        query += ' AND flight_status = \'%s\'' % (flightStatus)

    if planeID:
        query += ' AND airplane_id = \'%s\'' % (planeID)

    if basePrice:
        query += ' AND base_price = \'%s\'' % (basePrice)
    

    print(query)
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    if not data:
        error = "No flights found."
        return render_template('staff_flight_search.html', error = error)
    else:
        return render_template('staff_flight_search.html', data = data)


@app.route('/staff_create_auth', methods=['GET', 'POST'])
def staff_create_auth():
    flightNum = request.form['flightNum']
    departureDate  = request.form['departureDate']
    arrivalDate = request.form['arrivalDate']
    departureCode = request.form['departureCode']
    arrivalCode  = request.form['arrivalCode']
    basePrice   = request.form['basePrice']
    flightStatus = request.form['flightStatus']
    planeID = request.form['planeID']
    username = session.get('username')

    cursor = conn.cursor()
    
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_flight_create.html', error = error)

    airline_name = authdata['airline_name']

    query = 'SELECT airport_code FROM airport WHERE airport_code = %s'
    cursor.execute(query, (departureCode))
    departCodeCheckData = cursor.fetchone()

    if not departCodeCheckData:
        error = 'Departure airport does not exist!'
        return render_template('staff_flight_create.html', error = error)
    
    query = 'SELECT airport_code FROM airport WHERE airport_code = %s'
    cursor.execute(query, (arrivalCode))
    arrivalCodeCheckData = cursor.fetchone() 

    if not arrivalCodeCheckData:
        error = 'Arrival airport does not exist!'
        return render_template('staff_flight_create.html', error = error)

    query = 'SELECT * FROM airplane WHERE airplane_id = %s AND airline_name = %s'
    cursor.execute(query, (planeID, airline_name))
    planeCheckData = cursor.fetchone() 

    if not planeCheckData:
        error = 'The airplane provided does not exist!'
        return render_template('staff_flight_create.html', error = error)

    query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date_time = %s'
    cursor.execute(query, (airline_name, flightNum, departureDate))
    existingFlight = cursor.fetchone()

    if existingFlight:
        error = 'This flight already exists!'
        return render_template('staff_flight_create.html', error = error)

    query = 'SELECT * FROM flight WHERE airline_name = %s AND airplane_id = %s AND %s <= ' \
            'arrival_date_time AND departure_date_time <= %s'

    cursor.execute(query, (airline_name, planeID, departureDate, arrivalDate))
    planeInUse = cursor.fetchone()

    if planeInUse:
        error = 'Airplane with ID ' + planeID + ' is already in use that time!'
        return render_template('staff_flight_create.html', error = error)

    query = 'INSERT INTO flight values' \
        '((SELECT airline_name FROM airline WHERE airline_name = %s),' \
        '%s, %s, ' \
        '(SELECT airport_code FROM airport WHERE airport_code = %s),' \
        '(SELECT airport_code FROM airport WHERE airport_code = %s),' \
        '%s, %s, %s, %s)' 
    
    cursor.execute(query, (airline_name, flightNum, departureDate, departureCode, \
        arrivalCode, arrivalDate, flightStatus, planeID, basePrice))

    conn.commit()
    cursor.close()

    success = "Flight created!"
    return render_template('staff_flight_create.html', success=success)


@app.route('/staff_change_auth', methods=['GET', 'POST'])
def staff_change_auth():
    flightNum = request.form['flightNum']
    departureDate  = request.form['departureDate']
    status = request.form['statuses']

    error = None
    cursor = conn.cursor()
    username = session.get('username')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_change_status.html', error = error)
    
    airline_name = authdata['airline_name']

    existquery = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date_time = %s'
    cursor.execute(existquery, (airline_name, flightNum, departureDate))

    existdata = cursor.fetchone()

    if not existdata:
        error = 'That flight does not exist!'
        return render_template('staff_change_status.html', error = error)

    query = 'UPDATE flight SET flight_status = %s '\
            'WHERE airline_name = %s AND flight_number = %s AND departure_date_time = %s'
    
    cursor.execute(query, (status, airline_name, flightNum, departureDate))
    conn.commit()
    cursor.close()
    success = 'Status for flight #' + flightNum + ' was successfully changed to ' + status  
    return render_template('staff_change_status.html', success = success)


@app.route('/staff_create_plane_auth', methods=['GET', 'POST'])
def staff_create_plane_auth():
    planeID = request.form['airplaneId']
    numSeats  = request.form['numSeats']
    planeAge = request.form['planeAge']
    manufacturer = request.form['manufacturer']

    error = None
    cursor = conn.cursor()
    username = session.get('username')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_plane_create.html', error = error)
    
    airline_name = authdata['airline_name']

    query = 'SELECT * FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    ownedPlanes = cursor.fetchall()

    query = 'SELECT * FROM airplane WHERE airplane_id = %s AND airline_name = %s'
    cursor.execute(query, (planeID, airline_name))
    existingPlane = cursor.fetchone()

    if existingPlane:
        error = 'That airplane ID already exists!'
        return render_template('staff_plane_create.html', ownedPlanes = ownedPlanes, error = error)
    
    query = 'INSERT INTO airplane values (%s, (SELECT airline_name FROM airline WHERE airline_name = %s), %s, %s, %s)'
    cursor.execute(query, (planeID, airline_name, numSeats, planeAge, manufacturer))
    conn.commit()

    query = 'SELECT * FROM airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    ownedPlanes = cursor.fetchall()
    cursor.close()


    success = 'New airplane successfully added!'
    return render_template('staff_plane_create.html', success = success, ownedPlanes = ownedPlanes)


@app.route('/staff_create_airport_auth', methods=['GET', 'POST'])
def staff_create_airport_auth():
    airportcode = request.form['airportcode']
    airportname  = request.form['airportname']
    city = request.form['city']
    country = request.form['country']
    airport_type = request.form['airport_type']

    error = None
    cursor = conn.cursor()
    username = session.get('username')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_airport_create.html', error = error)

    query = 'SELECT * FROM airport WHERE airport_code = %s'
    cursor.execute(query, (airportcode))
    airportExists = cursor.fetchone()

    if airportExists:
        error = 'Airport code already exists!'
        return render_template('staff_airport_create.html', error = error)
    
    query = 'INSERT INTO airport values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (airportcode, airportname, city, country, airport_type))
    conn.commit()
    cursor.close()

    success = 'New airport ' + airportcode + ' successfully added!'
    return render_template('staff_airport_create.html', success=success) 


@app.route('/staff_rating_auth', methods=['GET', 'POST'])
def staff_rating_auth():
    airline_name = request.form['airline_name']
    cust_email = request.form['customer_email']
    flightNum  = request.form['flightNum']
    departure_date = request.form['departureDate']

    error = None
    cursor = conn.cursor()
    username = session.get('username')
    if not username:
        return redirect('/')

    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_rating_view.html', error = error)

    # Check if flight existed
    flightExistsQuery = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date_time = %s'
    cursor.execute(flightExistsQuery, (airline_name, flightNum, departure_date))
    flightExists = cursor.fetchone()

    if not flightExists:
        error = 'That flight does not exist!'
        return render_template('staff_rating_view.html', error = error)

    averageQuery = 'SELECT AVG(rating) FROM (SELECT * FROM rating WHERE airline_name = %s AND departure_date_time = %s) as avgRating'
    cursor.execute(averageQuery, (airline_name, departure_date))
    average_rating = cursor.fetchone()

    if average_rating['AVG(rating)'] == None:
        average_rating = 'Not available'
    else:
        average_rating = str(round(average_rating['AVG(rating)'],2))

    ratinglist = []

    if cust_email:
        query = 'SELECT * FROM rating WHERE customer_email = %s AND airline_name = %s AND flight_number = %s AND departure_date_time = %s'
        cursor.execute(query, (cust_email, airline_name, flightNum, departure_date))
        customer_rev = cursor.fetchone()

        if customer_rev == None:
            error = 'No ratings or reviews found for ' + airline_name + ' ' + flightNum + ' ' + departure_date + ' from ' + cust_email
            return render_template('staff_rating_view.html', error = error)
        
        ratinglist.append(customer_rev)

    else:
        query = 'SELECT * FROM rating WHERE airline_name = %s AND flight_number = %s AND departure_date_time = %s'
        cursor.execute(query, (airline_name, flightNum, departure_date))
        ratinglist = cursor.fetchall()

        if len(ratinglist) == 0:
            error = 'No ratings or reviews found for ' + airline_name + ' ' + flightNum + ' ' + departure_date
            return render_template('staff_rating_view.html', error = error)

    success = 'Loaded reviews for ' + airline_name + ' ' + flightNum + ' ' + departure_date
    return render_template('staff_rating_view.html', ratinglist = ratinglist, average_rating = average_rating, success=success)


@app.route('/staff_frequentcust_view_auth', methods=['GET', 'POST'])
def staff_frequentcust_view_auth():
    # Check if logged in
    username = session.get('username')
    if not username:
        return redirect('/')

    # Authenticate Staff Query
    cursor = conn.cursor()
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # Failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_frequentcust_view.html', error = error)
    
    airline_name = authdata['airline_name']
    customer_email = request.form['customer_email']

    # Most Freq
    query = 'SELECT customer_email, COUNT(*) as numCount FROM ticket WHERE airline_name = %s AND '\
        'purchase_date_time >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR) AND ' \
        'purchase_date_time <= DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) AND sold_price is not null GROUP BY customer_email ORDER BY numCount DESC LIMIT 3'

    cursor.execute(query, (airline_name))
    most_frequent_customers = cursor.fetchall()

    query = 'SELECT * FROM ticket WHERE airline_name = %s AND customer_email = %s'
    cursor.execute(query, (airline_name, customer_email))
    customerTickets = cursor.fetchall()
    if len(customerTickets) == 0:
        error = 'Could not find any purchases or flights that customer has been on!'
        return render_template('staff_frequentcust_view.html', error = error, most_frequent_customers = most_frequent_customers)

    cursor.close()

    if len(most_frequent_customers) == 0:
        none_frequent = 'No frequent customers within the last year...'
        return render_template('staff_frequentcust_view.html', customerTickets = customerTickets, none_frequent = none_frequent)

    return render_template('staff_frequentcust_view.html', customerTickets = customerTickets, most_frequent_customers = most_frequent_customers)


@app.route('/staff_reports_view_auth', methods=['GET', 'POST'])
def staff_reports_view_auth():
    from_date = request.form['fromDate']
    to_date  = request.form['toDate']

    # Check if logged in
    username = session.get('username')
    if not username:
        return redirect('/')

    # Authenticate Staff Query
    cursor = conn.cursor()
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # Failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_reports_view.html', error = error)
    
    airline_name = authdata['airline_name']
    query = 'SELECT COUNT(*) as num FROM ticket WHERE purchase_date_time BETWEEN %s AND %s AND airline_name = %s AND sold_price IS NOT NULL'
    cursor.execute(query, (from_date, to_date, airline_name))

    numTickets = cursor.fetchone()

    query = 'SELECT YEAR(purchase_date_time) as purchase_year, MONTH(purchase_date_time) as purchase_month, ' \
            'COUNT(*) as num FROM ticket WHERE purchase_date_time BETWEEN %s AND %s AND airline_name = %s AND sold_price IS NOT NULL ' \
            'GROUP BY YEAR(purchase_date_time), MONTH(purchase_date_time)'
    
    cursor.execute(query, (from_date, to_date, airline_name))
    monthlyTickets = cursor.fetchall()

    cursor.close()
    print(numTickets)
    if numTickets == None or numTickets['num'] == 0:
        error = 'No tickets found for that range.'
        return render_template('staff_reports_view.html', error = error)


    return render_template('staff_reports_view.html', numTickets = numTickets['num'], monthlyTickets = monthlyTickets)


@app.route('/checkFlight', methods=['GET', 'POST'])
def checkFlight():
    username = session['username']
    query = "SELECT first_name, last_name FROM customer WHERE customer_email = %s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    firstname = data2[0]['first_name']
    lastname = data2[0]['last_name']
    cursor.close()
    source = request.form['source']
    destination = request.form['destination']
    return_date = request.form['return_date']
    departure = request.form['departure']
    now = datetime.now()
    time = now.strftime("%m/%d/%Y, %H:%M:%S")
    if time > departure:
        error = "You can't book past flights"
        return render_template('checkandbook.html', error2=error, firstname=firstname, lastname=lastname)
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'
    cursor.execute(query, (source, destination, departure))
    # stores the results in a variable
    data1 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    cursor = conn.cursor()
    result2 = None
    data2 = None
    print(time > departure)
    if return_date:
        if return_date < departure:
            error = "not valid time range"
            return render_template('checkandbook.html', error2=error, firstname=firstname, lastname=lastname)
        else:
            query = 'SELECT * FROM flight WHERE departure_airport_code = %s and arrival_airport_code = %s and departure_date_time >= %s'
            cursor.execute(query, (destination, source, return_date))
            data2 = cursor.fetchall()
            cursor.close()

    error = None
    result = []
    result2 = []
    if (data1):
        # creates a session for the the user
        # session is a built in
        for i in data1:
            result.append(
                "airline: " + i["airline_name"] + " ; flight number: " + i["flight_number"] + " ; depart time: " + i[
                    "departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S") + "; arrival time: " + i[
                    "arrival_date_time"].strftime("%m/%d/%Y, %H:%M:%S"))
        if data2:
            for i in data2:
                result2.append(
                    "airline: " + i["airline_name"] + " ; flight number: " + i["flight_number"] + " ; depart time: " +
                    i["departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S") + "; arrival time: " + i[
                        "arrival_date_time"])
            return render_template('checkandbook.html', result2=result, result3=result2, firstname=firstname,
                                   lastname=lastname)
        else:
            if return_date:
                result2 = "we currently do not have return flight for you"
                return render_template('checkandbook.html', result2=result, result3=result2, firstname=firstname,
                                       lastname=lastname)
            else:
                return render_template('checkandbook.html', result2=result, firstname=firstname, lastname=lastname)
    else:
        # returns an error message to the html page
        error = 'such flight does not exist'
        return render_template('checkandbook.html', error2=error, firstname=firstname, lastname=lastname)


@app.route('/checkownAuth', methods=['GET', 'POST'])
def checkownAuth():
    username = session['username']
    now = datetime.now()
    time = now.strftime("%Y-%m-%d")
    cursor = conn.cursor()
    query = "SELECT * From Ticket WHERE customer_email = %s and departure_date_time >= %s and sold_price is not null"
    cursor.execute(query, (username, time))
    data = cursor.fetchall()
    cursor.close()
    query = "SELECT first_name, last_name FROM customer WHERE customer_email = %s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    firstname = data2[0]['first_name']
    lastname = data2[0]['last_name']
    cursor.close()
    res = []
    if (data):
        # creates a session for the the user
        # session is a built in
        for i in data:
            res.append("ticket ID: " + i["ticket_id"] + " airline: " + i["airline_name"] + " ; flight number: " + i[
                "flight_number"] + " ; depart time: " + i["departure_date_time"].strftime("%m/%d/%Y, %H:%M:%S"))
        return render_template('checkcancelandcomment.html', result=res, firstname=firstname, lastname=lastname)
    else:
        # returns an error message to the html page
        error = 'You do not have any booked future booked flights'
        return render_template('checkcancelandcomment.html', error=error, firstname=firstname, lastname=lastname)


def checkCapacity(airlinename, flight_num):
    cursor = conn.cursor()
    query = "SELECT airplane_id From Flight WHERE airline_name = %s and flight_number = %s"
    cursor.execute(query, (airlinename, flight_num))
    data = cursor.fetchone()
    query = "SELECT num_seats From Airplane WHERE airline_name = %s and airplane_id = %s"
    cursor.execute(query, (airlinename, data['airplane_id']))
    data = cursor.fetchone()
    cursor.close()
    return data


def checkSoldPrice(airlinename, flight_num, depart_time):
    num_seat = checkCapacity(airlinename, flight_num)
    query = "SELECT COUNT(*) FROM ticket WHERE airline_name = %s and flight_number = %s and departure_date_time = %s"
    cursor = conn.cursor()
    cursor.execute(query, (airlinename, flight_num, depart_time))
    sale = cursor.fetchone()
    query = "SELECT COUNT(*) FROM ticket WHERE airline_name = %s and flight_number = %s and departure_date_time = %s and sold_price is not null"
    cursor.execute(query, (airlinename, flight_num, depart_time))
    valid_sale = cursor.fetchone()
    print(num_seat, sale)
    if not num_seat:
        return None, None
    if (valid_sale['COUNT(*)'] - num_seat['num_seats']) == 0:
        return None, None
    query = "SELECT base_price From Flight WHERE airline_name = %s and flight_number = %s and departure_date_time = %s"
    cursor = conn.cursor()
    cursor.execute(query, (airlinename, flight_num, depart_time))
    data = cursor.fetchone()

    if not data:
        return None, None
    price = data['base_price']
    cursor.close()
    if sale['COUNT(*)'] / num_seat['num_seats'] >= 0.75:
        return float(price) * 1.25, 1000 * int(flight_num) + num_seat['num_seats'] - sale['COUNT(*)']
    else:
        return float(price) * 1, 1000 * int(flight_num) + num_seat['num_seats'] - sale['COUNT(*)']


@app.route('/bookTickets', methods=['GET', 'POST'])
def bookTickets():
    username = session['username']
    airline = request.form['airline']
    flight_num = request.form['flight_number']
    departure_date = request.form['departure']
    card_type = request.form['cardType']
    card_number = request.form['cardNumber']
    cardHolderFirstName = request.form['cardHolderFirstName']
    cardHolderLastName = request.form['cardHolderLastName']
    expirationDate = request.form['expirationDate']
    TravelClass = request.form['TravelClass']
    cursor = conn.cursor()
    purchase_date = datetime.now().strftime("%Y-%m-%d")
    soldprice, ticket_id = checkSoldPrice(airline, flight_num, departure_date)
    print(expirationDate,purchase_date,departure_date)
    if expirationDate < purchase_date:
        result = "Your Card Has Expired!"
        return render_template('checkandbook.html', result4=result)
    if departure_date < datetime.now().strftime("%Y-%m-%dT%H:%M:%S"):
        result = "You can't purchase past flight!"
        return render_template('checkandbook.html', result4=result)
    if not soldprice:
        result = "No Tickets Available Right Now..."
        return render_template('checkandbook.html', result4=result)
    ticket_query = 'INSERT INTO Ticket (ticket_id,airline_name,flight_number,departure_date_time,customer_email,travel_class,sold_price,card_type,card_num,card_first_name,card_last_name,card_expiration,purchase_date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(ticket_query, (
    ticket_id, airline, flight_num, departure_date, username, TravelClass, soldprice, card_type, card_number,
    cardHolderFirstName, cardHolderLastName, expirationDate, datetime.now()))
    purchase_query = 'INSERT INTO Purchase Values(%s,%s)'
    cursor.execute(purchase_query, (ticket_id, username))
    conn.commit()
    cursor.close()

    query = "SELECT first_name, last_name FROM customer WHERE customer_email = %s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    firstname = data2[0]['first_name']
    lastname = data2[0]['last_name']
    cursor.close()
    return render_template('checkandbook.html', result4="Successly booked", firstname=firstname, lastname=lastname)


def checkTicket(ticket_id, username):
    departure_query = "SELECT customer_email,departure_date_time FROM ticket WHERE ticket_id = %s and sold_price is not null"
    cursor = conn.cursor()
    cursor.execute(departure_query, (ticket_id))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return "please give a valid ticket ID or this ticket has already been cancelled"
    departure = result["departure_date_time"]
    user_email = result["customer_email"]
    current_time = datetime.today().replace(microsecond=0)
    print(departure, current_time, (current_time - departure).days)
    if user_email != username:
        return "You do not have this ticket"
    if current_time > departure:
        return "You can't cancel past flight"
    if (departure - current_time).days < 1:
        return "It is too late to cancel your ticket"
    return


@app.route('/cancelTickets', methods=['GET', 'POST'])
def cancelTickets():
    cursor = conn.cursor()
    username = session['username']
    query = "SELECT first_name, last_name FROM customer WHERE customer_email = %s"
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    firstname = data2[0]['first_name']
    lastname = data2[0]['last_name']
    ticket_id = request.form["ticketID"]
    result = checkTicket(ticket_id, username)
    if result:
        return render_template('checkcancelandcomment.html', result5=result, firstname=firstname, lastname=lastname)
    query = "UPDATE ticket SET sold_price = NULL WHERE ticket_id = %s"
    cursor.execute(query, (ticket_id))
    conn.commit()
    cursor.close()
    return render_template('checkcancelandcomment.html', result5="Cancelled Successfully", firstname=firstname,
                           lastname=lastname)


def checkIftaken(username, ticket_id):
    departure_query = "SELECT customer_email,departure_date_time FROM ticket WHERE ticket_id = %s and sold_price is not null"
    cursor = conn.cursor()
    cursor.execute(departure_query, (ticket_id))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return "please give a valid ticket ID"
    departure = result["departure_date_time"]
    user_email = result["customer_email"]
    current_time = datetime.today().replace(microsecond=0)
    if user_email != username:
        return "You do not have this ticket"
    if departure > current_time:
        return "You are not even on this plane yet!"
    return


def getFlightinfoFromTicket(ticket_id):
    cursor = conn.cursor()
    query = "SELECT airline_name,flight_number,departure_date_time FROM ticket WHERE ticket_id = %s"
    cursor.execute(query, (ticket_id))
    result = cursor.fetchone()
    cursor.close()
    return result["airline_name"], result["flight_number"], result["departure_date_time"]


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    cursor = conn.cursor()
    username = session['username']
    query = "SELECT first_name, last_name FROM customer WHERE customer_email = %s"
    cursor.execute(query, (username))
    data2 = cursor.fetchall()
    firstname = data2[0]['first_name']
    lastname = data2[0]['last_name']
    ticket_id = request.form["ticketID"]
    rate = request.form["rate"]
    comment = request.form["comment"]
    result = checkIftaken(username, ticket_id)
    if result:
        return render_template('checkcancelandcomment.html', result6=result, firstname=firstname, lastname=lastname)
    query = 'INSERT INTO rating Values(%s,%s,%s,%s,%s,%s)'
    airline, flight, departure = getFlightinfoFromTicket(ticket_id)
    try:
        cursor.execute(query, (username, airline, flight, departure, comment, rate))
    except:
        return render_template('checkcancelandcomment.html', result6="you have commented", firstname=firstname,
                               lastname=lastname)
    conn.commit()
    cursor.close()
    return render_template('checkcancelandcomment.html', result6="Rated Successfully", firstname=firstname,
                           lastname=lastname)


@app.route('/track', methods=['GET', 'POST'])
def track():
    username = session['username']
    query = "SELECT sum(sold_price) FROM ticket where (purchase_date_time > DATE_SUB(now(), INTERVAL 6 MONTH)) and customer_email = %s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data = cursor.fetchall()
    query = "SELECT ticket_id,purchase_date_time,sold_price FROM ticket where (purchase_date_time > DATE_SUB(now(), INTERVAL 6 MONTH)) and customer_email = %s and sold_price is not null"
    cursor.execute(query, (username))
    res = cursor.fetchall()
    cursor.close()
    return render_template('checkspending.html', result=str(data[0]["sum(sold_price)"]) + "$", result3 = res)


@app.route('/track2', methods=['GET', 'POST'])
def track2():
    username = session['username']
    start_range = request.form['start_range']
    end_range = request.form['end_range']
    query = "SELECT sum(sold_price) FROM ticket where (purchase_date_time between %s and %s) and customer_email = %s"
    cursor = conn.cursor()
    cursor.execute(query, (start_range, end_range, username))
    data = cursor.fetchall()
    query = "SELECT ticket_id,purchase_date_time,sold_price FROM ticket where (purchase_date_time between %s and %s) and customer_email = %s and sold_price is not null"
    cursor.execute(query, (start_range, end_range, username))
    res = cursor.fetchall()
    cursor.close()
    if not data[0]["sum(sold_price)"]:
        result = "0"
        return render_template('checkspending.html', result2=result + "$")
    return render_template('checkspending.html', result2=str(data[0]["sum(sold_price)"]) + "$",result3 = res)

@app.route('/staff_addphone_auth', methods=['GET', 'POST'])
def staff_addphone_auth():
    # Check if logged in
    username = session.get('username')
    if not username:
        return redirect('/')

    # Authenticate Staff Query
    cursor = conn.cursor()
    authquery = 'SELECT * FROM airlinestaff WHERE user_name = %s'
    cursor.execute(authquery, (username))
    authdata = cursor.fetchone()

    # Failed authentication of session
    if not authdata:
        error = 'Invalid staff member'
        return render_template('staff_addphone.html', error = error)

    airline_name = authdata['airline_name']
    phone_number = request.form['phone_number']
    alreadyExistQuery = 'SELECT * FROM phonenumber WHERE user_name = %s AND phone_num = %s'

    cursor.execute(alreadyExistQuery, (username, phone_number))
    exists = cursor.fetchone()

    if exists:
        error = 'Number already on file!'
        return render_template('staff_addphone.html', error = error)

    query = 'INSERT INTO phonenumber VALUES ((SELECT user_name FROM airlinestaff WHERE user_name = %s), %s)'
    cursor.execute(query, (username, phone_number))
    conn.commit()
    cursor.close()
    success = 'New number was added successfully!'
    return render_template('/staff_addphone.html', success=success)

@app.route('/logout')
def logout():
    username = session.get('username')
    if not username:
        return redirect('/')

    session.pop('username')
    return render_template('index.html', message='Goodbye!', success='Successfully logged out!')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
