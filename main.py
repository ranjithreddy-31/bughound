from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__)

def get_connection():
	return mysql.connector.connect(user='root', password='', host='localhost', database='bughound')

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
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Execute query
        query = "INSERT INTO employees (name, username, password, userlevel) VALUES (%s, %s, %s, %s)"
        values = (name, username, password, userlevel)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "success"
    except Exception as e:
	    return f"failed:{e}"
@app.route('/delete_employee_form')
def delete_employee_form():
	return render_template('delete_employee.html')
@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    # Fetch form data
    username = request.form['username']
    password = request.form['password']
    employee_id = int(request.form['employee_id'])
    # Connect to database
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Execute query
        query = f"select password from employees where username='{username}'"
        cursor.execute(query)
        db_password = cursor.fetchall()[0][0]
        if password == db_password:
            query = f"delete from employees where emp_id={employee_id}"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            return f"Successfully deleted employee:{employee_id}"
        else:
            cursor.close()
            conn.close()
            return "Invalid credentials"
    except Exception as e:
	    return f"failed:No employee id in the database (technical reason:{e})"
@app.route('/update_employee_form')
def update_employee_form():
	return render_template('update_employee.html')


@app.route('/update_employee', methods=['POST'])
def update_employee():
	username = request.form['username']
	password = request.form['password']
	employee_id = int(request.form['employee_id'])
	new_name = request.form['new_name']
	new_username = request.form['new_username']
	new_password = request.form['new_password']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"select password from employees where username='{username}'"
		cursor.execute(query)
		db_password = cursor.fetchall()[0][0]
		if password == db_password:
			if new_name:
				query = f"update employees set name='{new_name}' where emp_id = {employee_id}"
				print(query)
				cursor.execute(query)
				conn.commit()
			if new_username:
				query = f"update employees set username='{new_username}' where emp_id = {employee_id}"
				print(query)
				cursor.execute(query)
				conn.commit()
			if new_password:
				query = f"update employees set password='{new_password}' where emp_id = {employee_id}"
				print(query)
				cursor.execute(query)
				conn.commit()
			cursor.close()
			conn.close()
			return f"successfully updated employee:{employee_id}"
		else:
			cursor.close()
			conn.close()
			return "Failed updating: Invalid Password"

	except Exception as e:
		return f"failed:No employee id in the database (technical reason:{e})"

@app.route('/program')
def program():
 	return render_template('program.html')

@app.route('/add_program_form')
def add_program_form():
	return render_template('add_program.html')

@app.route('/add_program', methods=['POST'])
def add_program():
	program = request.form['program']
	version = request.form['version']
	release = request.form['release']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = "INSERT INTO programs (program, program_release, program_version) VALUES (%s, %s, %s)"
		values = (program,version,release)
		cursor.execute(query,values)
		conn.commit()
		cursor.close()
		conn.close()
		return "success"
	except Exception as e:
		return f"failed:{e}"
@app.route('/update_program_form')
def update_program_form():
	return render_template('update_program.html')

@app.route('/update_program', methods=['POST'])
def update_program():
	username = request.form['username']
	password = request.form['password']
	program_id = int(request.form['program_id'])
	new_name = request.form['new_name']
	new_release = request.form['new_release']
	new_version = request.form['new_version']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"select password from employees where username='{username}'"
		cursor.execute(query)
		db_password = cursor.fetchall()[0][0]
		if password == db_password:
			if new_name:
				query = f"update programs set program='{new_name}' where prog_id = {program_id}"
				cursor.execute(query)
				conn.commit()
			if new_release:
				query = f"update programs set program_release='{new_release}' where prog_id = {program_id}"
				cursor.execute(query)
				conn.commit()
			if new_version:
				query = f"update programs set program_version='{new_version}' where prog_id = {program_id}"
				cursor.execute(query)
				conn.commit()
			cursor.close()
			conn.close()
			return f"successfully updated employee:{program_id}"
		else:
			cursor.close()
			conn.close()
			return "Failed updating: Invalid Password"

	except Exception as e:
		return f"failed:No employee id in the database (technical reason:{e})"

@app.route('/delete_program_form')
def delete_program_form():
	return render_template('delete_program.html')

@app.route('/delete_program', methods=['POST'])
def delete_program():
    # Fetch form data
    username = request.form['username']
    password = request.form['password']
    program_id = int(request.form['program_id'])
    # Connect to database
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Execute query
        query = f"select password from employees where username='{username}'"
        cursor.execute(query)
        db_password = cursor.fetchall()[0][0]
        if password == db_password:
            query = f"delete from programs where prog_id={program_id}"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            return f"Successfully deleted program:{program_id}"
        else:
            cursor.close()
            conn.close()
            return "Invalid credentials"
    except Exception as e:
	    return f"failed:No program id in the database (technical reason:{e})"
if __name__ == '__main__':
	app.run(debug=True)
