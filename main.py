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
			query = f"delete from bug where reoported_by={employee_id};"
			cursor.execute(query)
			query = f"delete from bug where assigned_to={employee_id};"
			cursor.execute(query)
			query = f"delete from bug where resolved_by={employee_id};"
			cursor.execute(query)
			query = f"delete from employees where tested_by={employee_id};"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			conn.close()
			return f"Successfully deleted employee:{employee_id};"
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
			return f"successfully updated Program:{program_id}"
		else:
			cursor.close()
			conn.close()
			return "Failed updating: Invalid Password"

	except Exception as e:
		return f"failed:No program id in the database (technical reason:{e})"

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
			query = f"delete from areas where prog_id={program_id}"
			cursor.execute(query)
			query = f"delete from bug where program_id = {program_id};"
			cursor.execute(query)
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
@app.route('/area')
def area():
 	return render_template('area.html')

@app.route('/add_area_form')
def add_area_form():
	return render_template('add_area.html')

@app.route('/add_area', methods = ["POST"])
def add_area():
	area = request.form['area']
	prog_id = int(request.form['prog_id'])
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"select prog_id from programs where prog_id='{prog_id}'"
		cursor.execute(query)
		if not cursor.fetchall():
			return 'Program ID entered does not exist in Database!'
		else:
			query = "INSERT INTO areas (area, prog_id) VALUES (%s, %s)"
			values = (area,prog_id)
			cursor.execute(query, values)
			conn.commit()
			cursor.close()
			conn.close()
			return "success"
	except Exception as e:
		return f"failed:{e}"

@app.route('/update_area_form')
def update_area_form():
	return render_template('update_area.html')

@app.route('/update_area', methods=['POST'])
def update_area():
	username = request.form['username']
	password = request.form['password']
	area_id = int(request.form['area_id'])
	new_name = request.form['new_name']
	new_prog_id = request.form['new_prog_id']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"select password from employees where username='{username}'"
		cursor.execute(query)
		db_password = cursor.fetchall()[0][0]
		if password == db_password:
			if new_prog_id:
				query = f"select prog_id from programs where prog_id='{new_prog_id}'"
				cursor.execute(query)
				if not cursor.fetchall():
					return 'New Program ID entered does not exist in Database!'
				else:
					query = f"update areas set prog_id='{new_prog_id}' where area_id = {area_id}"
					cursor.execute(query)
					conn.commit()

			if new_name:
				query = f"update areas set area='{new_name}' where area_id = {area_id}"
				cursor.execute(query)
				conn.commit()
			cursor.close()
			conn.close()
			return f"successfully updated Area:{area_id}"
		else:
			cursor.close()
			conn.close()
			return "Failed updating: Invalid Password"

	except Exception as e:
		return f"failed:No Program id in the database (technical reason:{e})"



@app.route('/delete_area_form')
def delete_area_form():
	return render_template('delete_area.html')

@app.route('/delete_area', methods=['POST'])
def delete_area():
	# Fetch form data
	username = request.form['username']
	password = request.form['password']
	area_id = int(request.form['area_id'])
	# Connect to database
	try:
		conn = get_connection()
		cursor = conn.cursor()

		# Execute query
		query = f"select password from employees where username='{username}'"
		cursor.execute(query)
		db_password = cursor.fetchall()[0][0]
		if password == db_password:
			query = f"delete from areas where area_id={area_id}"
			cursor.execute(query)
			conn.commit()
			cursor.close()
			conn.close()
			return f"Successfully deleted Area:{area_id}"
		else:
			cursor.close()
			conn.close()
			return "Invalid credentials"
	except Exception as e:
		return f"failed:No Area id in the database (technical reason:{e})"
	
@app.route('/show_employees',methods=['GET','POST'])
def show_employees():
	try:
		conn = get_connection()
		cursor = conn.cursor()

		query = "select emp_id,name,username,userlevel from employees;"
		cursor.execute(query)
		data = []
		for (id, name, username,level) in cursor:
			data.append({'emp_id': id, 'name': name, 'username': username, 'level':level})
		cursor.close()
		conn.close()

		return render_template('employee_details.html', data=data)

	except Exception as e:
		return f"failed:No employee details found in the database (technical reason:{e})"
	
@app.route('/show_programs',methods=['GET','POST'])
def show_programs():
	try:
		conn = get_connection()
		cursor = conn.cursor()

		query = "select * from programs;"
		cursor.execute(query)
		data = []
		for (id, name, release,version) in cursor:
			data.append({'program_id': id, 'program': name, 'program_release': release, 'program_version':version})
		cursor.close()
		conn.close()

		return render_template('program_details.html', data=data)

	except Exception as e:
		return f"failed:No program details found in the database (technical reason:{e})"

@app.route('/show_areas',methods=['GET','POST'])
def show_areas():
	try:
		conn = get_connection()
		cursor = conn.cursor()

		query = "select a.area_id,a.prog_id,a.area,p.program from areas a natural join programs p;"
		cursor.execute(query)
		data = []
		for (a_id, p_id, area,program) in cursor:
			data.append({'a_id': a_id, 'p_id': p_id, 'area': area, 'program':program})
		cursor.close()
		conn.close()

		return render_template('area_details.html', data=data)

	except Exception as e:
		return f"failed:No area details found in the database (technical reason:{e})"
@app.route('/bug')
def bug():
 	return render_template('bug.html')

@app.route('/add_bug_form')
def add_bug_form():
	return render_template('add_bug.html')

@app.route('/add_bug', methods=['POST'])
def add_bug():

	program_id = request.form['program_id']
	report_type = request.form['report_type']
	severity = request.form['severity']
	problemSummary = request.form['problemSummary']
	reproducible = request.form['reproducible']
	suggested_fix = request.form['suggested_fix']
	reported_by = request.form['reported_by']
	reported_date = request.form['reported_date']
	functional_area = request.form['functional_area']
	assigned_to = request.form['assigned_to']
	comments = request.form['comments']
	status = request.form['status']
	priority = request.form['priority']

	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = "INSERT INTO bug (program_id, report_type, severity, problemSummary, reproducible, suggested_fix, reported_by, reported_date, functional_area, assigned_to, comments, status, priority) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s);"
		values = (program_id, report_type, severity, problemSummary, reproducible, suggested_fix, reported_by, reported_date, functional_area, assigned_to, comments, status, priority)
		cursor.execute(query,values)
		conn.commit()
		cursor.close()
		conn.close()
		return "success"
	except Exception as e:
		return f"failed:{e}"

@app.route('/close_bug_form')
def close_bug_form():
	return render_template('close_bug.html')

@app.route('/close_bug', methods=['POST'])
def close_bug():
	id  = int(request.form['id'])
	status = request.form['status']
	resolution = request.form['resolution']
	resolution_version = request.form['resolution_version']
	resolved_by = request.form['resolved_by']
	resolved_date = str(request.form['resolved_date'])
	tested_by = request.form['tested_by']
	tested_date = request.form['tested_date']
	defered = request.form['defered']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"update bug set status = '{status}', resolution = '{resolution}', resolution_version = '{resolution_version}', resolved_by = {resolved_by},resolved_date = '{resolved_date}', tested_by={tested_by}, tested_date = '{tested_date}',deferred = '{defered}' where id = {id}"
		print(query)
		cursor.execute(query)
		conn.commit()
		cursor.close()
		conn.close()
		return "success"
	except Exception as e:
		return f"failed:{e}"
	
@app.route('/search_bug_form',methods=['POST','GET'])
def search_bug_form():
	return render_template('search_bug.html')

@app.route('/search_bug', methods=['POST','GET'])
def search_bug():
	id  = request.form['id']
	quantity = request.form['quantity']
	priority = request.form['priority']
	status = request.form['status']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		query = f"select * from bug where {id} = {quantity} and priority = '{priority}' and status = '{status}';"
		print(query)
		cursor.execute(query)
		data = []
		for (id, program_id, report_type,severity,problemSummary,reproducible,suggested_fix,reported_by,reported_date,functional_area,assigned_to, comments,status, priority,resolution,resolution_version,resolved_by,resolved_date,tested_by,tested_date,deferred) in cursor:
			data.append({'id': id, 'program_id': program_id, 'report_type': report_type, 'severity':severity, 'problemSummary':problemSummary,'reproducible':reproducible,'suggested_fix':suggested_fix,'reported_by':reported_by,'reported_date':reported_date,'functional_area':functional_area,'assigned_to':assigned_to,'comments':comments,'status':status,'priority':priority,'resolution':resolution,'resolution_version':resolution_version,'resolved_by':resolved_by,'resolved_date':resolved_by,'tested_by':tested_by,'tested_date':tested_date,'deferred':deferred})
		cursor.close()
		conn.close()

		return render_template('bug_details.html', data=data)
	except Exception as e:
		return f"failed:{e}"

@app.route('/update_bug_form',methods=['POST','GET'])
def update_bug_form():
	return render_template('update_bug.html')

@app.route('/update_bug', methods=['POST','GET'])
def update_bug():
	id  = int(request.form['id'])
	program_id = request.form['program_id']
	report_type = request.form['report_type']
	severity = request.form['severity']
	problemSummary = request.form['problemSummary']
	reproducible = request.form['reproducible']
	suggested_fix = request.form['suggested_fix']
	reported_by = request.form['reported_by']
	reported_date = request.form['reported_date']
	functional_area = request.form['functional_area']
	assigned_to = request.form['assigned_to']
	comments = request.form['comments']
	status = request.form['status']
	priority = request.form['priority']
	resolution = request.form['resolution']
	resolution_version = request.form['resolution_version']
	resolved_by = request.form['resolved_by']
	resolved_date = str(request.form['resolved_date'])
	tested_by = request.form['tested_by']
	tested_date = request.form['tested_date']
	defered = request.form['defered']
	try:
		conn = get_connection()
		cursor = conn.cursor()
		if program_id:
			query = f"update bug set program_id={program_id} where id = {id}"
			cursor.execute(query)
		if report_type:
			query = f"update bug set report_type='{report_type}' where id = {id}"
			cursor.execute(query)
		if severity:
			query = f"update bug set severity='{severity}' where id = {id}"
			cursor.execute(query)
		if problemSummary:
			query = f"update bug set problemSummary='{problemSummary}' where id = {id}"
			cursor.execute(query)
		if reproducible:
			query = f"update bug set reproducible='{reproducible}' where id = {id}"
			cursor.execute(query)
		if suggested_fix:
			query = f"update bug set suggested_fix='{suggested_fix}' where id = {id}"
			cursor.execute(query)
		if reported_by:
			query = f"update bug set reported_by={reported_by} where id = {id}"
			cursor.execute(query)
		if reported_date:
			query = f"update bug set reported_date='{reported_date}' where id = {id}"
			cursor.execute(query)
		if functional_area:
			query = f"update bug set functional_area='{functional_area}' where id = {id}"
			cursor.execute(query)
		if assigned_to:
			query = f"update bug set assigned_to={assigned_to} where id = {id}"
			cursor.execute(query)
		if comments:
			query = f"update bug set comments='{comments}' where id = {id}"
			cursor.execute(query)
		if status:
			query = f"update bug set status='{status}' where id = {id}"
			cursor.execute(query)
		if priority:
			query = f"update bug set priority='{priority}' where id = {id}"
			cursor.execute(query)
		if resolution:
			query = f"update bug set resolution='{resolution}' where id = {id}"
			cursor.execute(query)
		if resolution_version:
			query = f"update bug set resolution_version='{resolution_version}' where id = {id}"
			cursor.execute(query)
		if resolved_by:
			query = f"update bug set resolved_by={resolved_by} where id = {id}"
			cursor.execute(query)
		if resolved_date:
			query = f"update bug set resolved_date='{resolved_date}' where id = {id}"
			cursor.execute(query)
		if tested_by:
			query = f"update bug set tested_by={tested_by} where id = {id}"
			cursor.execute(query)
		if tested_date:
			query = f"update bug set tested_date='{tested_date}' where id = {id}"
			cursor.execute(query)
		if defered:
			query = f"update bug set deferred='{defered}' where id = {id}"

		
		conn.commit()
		cursor.close()
		conn.close()
		return "Success"
	except Exception as e:
		return f"Updation of Bug failed due to {e}"

if __name__ == '__main__':
	app.run(debug=True)
