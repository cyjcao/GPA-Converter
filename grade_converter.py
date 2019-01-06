from app import app, db
from app.models import School, Grade
import json, os

# populate the school table if empty
# clear grade table
@app.before_first_request
def initialize_table():
	if School.query.first() is None:
		with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "app\static\schools.json"), "r") as read_file:
			school_data = json.load(read_file)
			for s in school_data:
				if type(s['scale']) is not list: 
					school = School(name=s['name'], scale=s['scale'])
					db.session.add(school)
					db.session.commit()
				else:
					scale = s['scale'][0] * 10 + s['scale'][1]
					school = School(name=s['name'], scale=scale)
					db.session.add(school)
					db.session.commit()
	
	Grade.query.delete()
	db.session.commit()