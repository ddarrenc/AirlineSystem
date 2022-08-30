/*
	Darren Chan
	Sicheng Xie
*/

CREATE TABLE airline (
    airline_name VARCHAR(25) NOT NULL,
    PRIMARY KEY (airline_name)
);

CREATE TABLE airport
(
	airport_code	VARCHAR(25) NOT NULL,
	airport_name	VARCHAR(25),
	city			VARCHAR(25),
	country			VARCHAR(25),
	type			VARCHAR(13)
		CHECK (type IN ('Domestic', 'International', 'Both')),

	PRIMARY KEY(airport_code)
);

CREATE TABLE airplane (
    airplane_id VARCHAR(25) NOT NULL,
    airline_name VARCHAR(25) NOT NULL,
    num_seats INT,
    plane_age INT,
    manufacturer VARCHAR(25),
    PRIMARY KEY (airplane_id, airline_name),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

CREATE TABLE flight
(
	airline_name	VARCHAR(25) NOT NULL,
	flight_number	VARCHAR(25) NOT NULL,
	departure_date_time	DATETIME NOT NULL,
	departure_airport_code	VARCHAR(25) NOT NULL,
	arrival_airport_code	VARCHAR(25) NOT NULL,
	arrival_date_time	DATETIME,
	flight_status	VARCHAR(25)
		CHECK (flight_status IN ('Delayed', 'On Time', 'Cancelled')),
	airplane_id	VARCHAR(25) NOT NULL,
	base_price	DECIMAL(10,2),

	PRIMARY KEY (airline_name, flight_number, departure_date_time),
	FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
		ON DELETE CASCADE,
	FOREIGN KEY (departure_airport_code) REFERENCES airport(airport_code)
		ON DELETE CASCADE,
	FOREIGN KEY (arrival_airport_code) REFERENCES airport(airport_code)
		ON DELETE CASCADE,
	FOREIGN KEY (airplane_id) REFERENCES airplane(airplane_id)
		ON DELETE CASCADE
);

CREATE TABLE customer (
    customer_email VARCHAR(25) NOT NULL,
    customer_password VARCHAR(200),
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    address_buildnum VARCHAR(25),
    address_street VARCHAR(25),
    address_city VARCHAR(25),
	address_state VARCHAR(25),
    passport_number VARCHAR(25),
    passport_expiration DATE,
    passport_country VARCHAR(25),
    date_of_birth DATE,
    phone_number VARCHAR(25),
    PRIMARY KEY (customer_email)
);

CREATE TABLE airlinestaff (
    user_name VARCHAR(25) NOT NULL,
    airline_name VARCHAR(25) NOT NULL,
    staff_password VARCHAR(200),
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    date_of_birth DATE,
    PRIMARY KEY (user_name),
    FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
		ON DELETE CASCADE
);

CREATE TABLE phonenumber (
    user_name VARCHAR(25) NOT NULL,
    phone_num VARCHAR(25) NOT NULL,
    PRIMARY KEY (phone_num, user_name),
    FOREIGN KEY (user_name) REFERENCES airlinestaff(user_name)
);

CREATE TABLE ticket (
	ticket_id VARCHAR(25) NOT NULL,
	airline_name VARCHAR(25) NOT NULL,
	flight_number VARCHAR(25) NOT NULL,
	departure_date_time DATETIME NOT NULL,
	customer_email VARCHAR(25) NOT NULL,
	travel_class VARCHAR(8)
		CHECK (travel_class IN ('First', 'Business', 'Economy')),
	sold_price DECIMAL(10,2),
	card_type VARCHAR(6)
		CHECK (card_type IN ('Credit', 'Debit')),
	card_num VARCHAR(25),
	card_first_name VARCHAR(25),
	card_last_name VARCHAR(25),
	card_expiration DATE,
	purchase_date_time DATETIME,

	PRIMARY KEY(ticket_id),
	FOREIGN KEY(airline_name, flight_number, departure_date_time) REFERENCES flight(airline_name, flight_number, departure_date_time)
		ON DELETE CASCADE,
	FOREIGN KEY (customer_email) REFERENCES customer(customer_email)
		ON DELETE CASCADE
);

CREATE TABLE rating (
	customer_email VARCHAR(25) NOT NULL,
	airline_name VARCHAR(25) NOT NULL,
	flight_number VARCHAR(25) NOT NULL,
	departure_date_time DATETIME NOT NULL,
	comments VARCHAR(25),
	rating DECIMAL(2,1),

	PRIMARY KEY(customer_email, airline_name, flight_number, departure_date_time),
	FOREIGN KEY(customer_email) REFERENCES customer(customer_email)
		ON DELETE CASCADE,
	FOREIGN KEY(airline_name, flight_number, departure_date_time) REFERENCES flight(airline_name, flight_number, departure_date_time)
		ON DELETE CASCADE
);

CREATE TABLE purchase (
	ticket_id VARCHAR(25) NOT NULL,
	customer_email VARCHAR(25) NOT NULL,
	PRIMARY KEY(ticket_id, customer_email),
    FOREIGN KEY (customer_email) REFERENCES customer(customer_email)
		ON DELETE CASCADE,
	FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
		ON DELETE CASCADE
);