from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class SchoolForm(FlaskForm):
	school = SelectField('School', validators=[DataRequired()], id='select_school')
	convert = SubmitField('Convert!')

class GradeForm(FlaskForm):
	course_name = StringField('Course', validators=[DataRequired()])
	credits = IntegerField('Credits', validators=[DataRequired()])
	grade = SelectField('Grade', validators=[DataRequired()])
	add = SubmitField('Add Grade')