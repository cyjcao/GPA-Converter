from app import app, db
from flask import render_template, url_for, redirect, session
from app.forms import SchoolForm, GradeForm
from app.models import School, Grade

selected = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	Grade.query.delete()
	db.session.commit()
	schools = []
	for row in School.query.all():
		school = {'name': row.name, 'scale': row.scale}
		schools.append(school)
	form = SchoolForm()
	
	# sort choices in alphabetical order
	form.school.choices = [(school['name'], school['name']) for school in sorted(schools, key=lambda k: k['name'])]
	if form.validate_on_submit():
		selected_school = form.school.data
		session['school_name'] = selected_school
		session['scale'] = School.query.filter_by(name=selected_school).first().scale
		
		return redirect(url_for('convert'))

	return render_template('index.html', form=form)

@app.route('/convert', methods=['GET', 'POST'])
def convert():
	school_name = session.get('school_name', None)
	scale = session.get('scale', 3)
	conversion_table = {}
	if scale == 9:
		conversion_table = {'A+': 4.00, 'A': 3.80, 'B+': 3.30, 'B': 3.00, 'C+': 2.30, 'C': 2.00, 'D+': 1.30, 
					'D': 1.00, 'E': 0.00, 'F': 0.00}
	elif scale == 8:
		conversion_table = {'A': 4.00, 'A-': 3.70, 'B+': 3.30, 'B': 3.00, 'B-': 2.70, 'C+': 2.30, 'C': 2.00, 
					'D+': 1.30, 'D': 1.00, 'D-': 0.70, 'E': 0.00, 'F': 0.00}
	elif scale == 7:
		conversion_table = {'A+': 4.00, 'A': 3.90, 'A-': 3.70, 'B+': 3.30, 'B': 3.00, 'B-': 2.70, 'C+': 2.30, 
					'C': 2.00, 'D+': 1.30, 'D': 1.00, 'D-': 0.70, 'E': 0.00, 'F': 0.00}
	elif scale == 6:
		conversion_table = {'94-100': 4.00, '85-93': 3.90, '80-84': 3.70, '75-79': 3.30, '70-74': 3.00, '65-69': 2.70, 
					'60-64': 2.30, '55-59': 2.00, '50-54': 1.00, '<= 49': 0.00}
	elif scale == 5:
		conversion_table = {'94-100': 4.00, '87-93': 3.90, '80-86': 3.70, '75-79': 3.30, '70-74': 3.00, '65-69': 2.70, 
					'60-64': 2.30, '55-59': 2.00, '50-54': 1.70, '<= 49': 0.00}
	elif scale == 4:
		conversion_table = {'93-100': 4.00, '84-92': 3.90, '75-83': 3.70, '72-74': 3.30, '69-71': 3.00, '66-68': 2.70, 
					'64-65': 2.30, '62-63': 2.00, '60-61': 1.70, '56-59': 1.30, '53-55': 1.00, '50-52': 0.70, '<= 49': 0.00}
	elif scale == 3:
		conversion_table = {'90-100': 4.00, '85-89': 3.90, '80-84': 3.70, '77-79': 3.30, '73-76': 3.00, '70-72': 2.70, 
					'67-69': 2.30, '63-66': 2.00, '60-62': 1.70, '57-59': 1.30, '53-56': 1.00, '50-52': 0.70, '<= 49': 0.00}
	elif scale == 37:
		conversion_table = {'A+ 90-100': 4.00, 'A 85-89': 3.90, 'A- 80-84': 3.70, 'B+ 77-79': 3.30, 'B 73-76': 3.00, 
					'B- 70-72': 2.70, 'C+ 67-69': 2.30, 'C 63-66': 2.00, 'C- 60-62': 1.70, 'D+ 57-59': 1.30, 
					'D 53-56': 1.00, 'D- 50-52': 0.70, 'E/F <= 49': 0.00}
	else:
		conversion_table = {'A+ 93-100': 4.00, 'A 84-92': 3.90, 'A- 75-83': 3.70, 'B+ 72-74': 3.30, 'B 69-71': 3.00, 
					'B- 66-68': 2.70, 'C+ 64-65': 2.30, 'C 62-63': 2.00, 'C- 60-61': 1.70, 'D+ 56-59': 1.30, 
					'D 53-55': 1.00, 'D- 50-52': 0.70, 'E/F <= 49': 0.00}
	
	grades, converted_gpa = convert_grades(conversion_table)
	grade_form = GradeForm()
	grade_form.grade.choices = [(key, key) for key in list(conversion_table.keys())]
	if grade_form.validate_on_submit():
		add_grade(grade_form)
		return redirect(url_for('convert'))

	return render_template('convert.html', school=school_name, grade_form=grade_form, grades=grades, gpa=converted_gpa)


def add_grade(grade_form):
	course = grade_form.course_name.data
	credits = grade_form.credits.data
	mark = grade_form.grade.data
	grade = Grade(course=course, credits=credits, grade=mark)
	db.session.add(grade)
	db.session.commit()

def convert_grades(conversion_table):
	grades = []
	total_credits = 0
	total_converted_grade = 0

	for row in Grade.query.all():
		converted_grade = conversion_table[row.grade]
		grade = (row.course, row.credits, row.grade, converted_grade)
		total_converted_grade = total_converted_grade + row.credits * converted_grade
		total_credits = total_credits + row.credits
		grades.append(grade)
	converted_gpa = None
	if(len(grades) > 0):
		converted_gpa = total_converted_grade / total_credits

	return grades, converted_gpa
