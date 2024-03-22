import pandas as pd
from per1 import PolicePerformance
from flask import Flask, render_template, request, jsonify
from ResponseMatrix import ResponseMatrix
from CrimeMatrix import CrimeMatrix
from IncidentMatrix import IncidentMatrix
from CommunityMatrix import CommunityMatrix
from TrendMatrix import TrendMatrix
from ResourceMatrix import ResourceMatrix
import hashlib  # For hashing passwords
from flask_mysqldb import MySQL
import hashlib  # For hashing passwords
import mysql.connector
from flask import redirect, url_for, session, flash

import matplotlib
matplotlib.use('Agg')

data = pd.read_csv('Copy of FIR_Details_Data.csv')

app = Flask(__name__)
app.secret_key = 'qwertyuioplkjhgfdsa'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Apekshashetty@29",
    database="ksp"
)
mycursor = mydb.cursor()


# Initialize MySQL
mysql = MySQL(app)
app.secret_key = 'sdfgfdsrtf'


districts = ['Bagalkot', 'Ballari', 'Belagavi City', 'Belagavi Dist',
             'Bengaluru City', 'Bengaluru Dist', 'Bidar', 'Chamarajanagar',
             'Chickballapura', 'Chikkamagaluru', 'Chitradurga', 'CID',
             'Coastal Security Police', 'Dakshina Kannada', 'Davanagere',
             'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Hubballi Dharwad City',
             'ISD Bengaluru', 'K.G.F', 'Kalaburagi', 'Kalaburagi City',
             'Karnataka Railways', 'Kodagu', 'Kolar', 'Koppal', 'Mandya',
             'Mangaluru City', 'Mysuru City', 'Mysuru Dist', 'Raichur',
             'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada',
             'Vijayanagara', 'Vijayapur', 'Yadgir']


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/home1', methods=['GET'])
def home1():
    return render_template('home1.html')

@app.route('/vision')
def vision():
    return render_template('vision.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


@app.route("/<district>", methods=["GET"])
def district_data(district):
    district = district.replace("-", " ")
    if district in districts:
        return render_template('bagalkot.html')
    else:
        return "District not found", 404


@app.route("/<district>/stations", methods=["GET"])
def district_station_data(district):
    district = district.replace("-", " ")
    x = data[data['District_Name'] == district].copy()
    ps = x["UnitName"].unique()
    if district in districts:
        return render_template("baglokotepoliice.html", ps=ps, district=district.replace(" ", "-"))
    else:
        return "Page not found", 404


@app.route("/<district>/stations/<station>", methods=["GET",  "POST"])
def district_station_police_data(district, station):
    district = district.replace("-", " ")
    station = station.replace("-", " ")
    if district in districts:
        if request.method == 'GET':
            return render_template('main.html')
        elif request.method == 'POST':
            req = request.get_json()
            name = req.get("name")
            pp = PolicePerformance(district, data, station)
            resp = pp.gef_officer_info(name)
            return jsonify(resp)


@app.route("/<district>/<performance>", methods=["GET"])
def performance_data(district, performance):
    district = district.replace("-", " ")
    title = f"{performance.capitalize()}"
    heading = f"{performance.capitalize()}"
    if district in districts:
        return render_template('index.html', img='', title=title, heading=heading)
    else:
        return "Invalid district", 404


@app.route("/<district>/<performance>/<graph>", methods=["GET"])
def performance_specific_data(district, performance, graph):
    district = district.replace("-", " ")
    if district in districts:
        img = ""
        if performance == "response Time Metrics":
            response_matrix = ResponseMatrix(district, data)
            if graph == 'line':
                img = response_matrix.create_line()
            elif graph == 'pie':
                img = response_matrix.create_pie()
            if graph == 'histogram':
                img = response_matrix.create_histogram()
        elif performance == "crime Clearance & Investigation Rates":
            crime_matrix = CrimeMatrix(district, data)
            if graph == 'line':
                img = crime_matrix.create_line()
            elif graph == 'pie':
                img = crime_matrix.create_pie()
            if graph == 'histogram':
                img = crime_matrix.create_histogram()
        elif performance == "incident Severity Metrics":
            incident_matrix = IncidentMatrix(district, data)
            if graph == 'line':
                img = incident_matrix.create_line()
            elif graph == 'pie':
                img = incident_matrix.create_pie()
            if graph == 'histogram':
                img = incident_matrix.create_histogram()
        elif performance == "community Engagement Metrics":
            community_matrix = CommunityMatrix(district, data)
            if graph == 'line':
                img = community_matrix.create_line()
            elif graph == 'pie':
                img = community_matrix.create_pie()
            if graph == 'histogram':
                img = community_matrix.create_histogram()
        elif performance == "trend & Pattern Analysis":
            trend_matrix = TrendMatrix(district, data)
            if graph == 'line':
                img = trend_matrix.create_line()
            elif graph == 'pie':
                img = trend_matrix.create_pie()
            if graph == 'histogram':
                img = trend_matrix.create_histogram()
        elif performance == "resource Allocation Metrics":
            resource_matrix = ResourceMatrix(district, data)
            if graph == 'line':
                img = resource_matrix.create_line()
            elif graph == 'pie':
                img = resource_matrix.create_pie()
            if graph == 'histogram':
                img = resource_matrix.create_histogram()
        return render_template('index.html', img=img)
    else:
        return "Invalid distrcict", 404
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        mycursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = mycursor.fetchone()

        if user:
            flash('Email already exists! Please use a different email.', 'danger')
            return redirect(url_for('register'))
        else:
            mycursor.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                             (first_name, last_name, email, password))
            mydb.commit()

            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = mycursor.fetchone()

        if user:
            session['logged_in'] = True
            session['email'] = email

            flash('Login successful!', 'success')
            return redirect(url_for('home1'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)