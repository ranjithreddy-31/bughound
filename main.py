from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')
@app.route('/employee')
def employee():
 	return render_template('employee.html')
@app.route('/register_employee_form')
def register_employee_form():
	return render_template('register_employee.html')
@app.route('/register_employee', methods=['POST'])
def register_employee():
    # Fetch form data
    #id = request.form['id']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    userlevel = request.form['userlevel']
    # Connect to database
    conn = mysql.connector.connect(user='root', password='',
                                    host='localhost', database='bughound')
    cursor = conn.cursor()

    # Execute query
    query = "INSERT INTO employees (name, username, password, userlevel) VALUES (%s, %s, %s, %s)"
    values = (name, username, password, userlevel)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return "success"


if __name__ == '__main__':
	app.run(debug=True)
