from app import db

class School(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), index=True, unique=True)
	scale = db.Column(db.Integer)

	def __repr__(self):
		return '<School name: {}>'.format(self.name)

class Grade(db.Model):
	course = db.Column(db.String(40), primary_key=True)
	credits = db.Column(db.Integer)
	grade = db.Column(db.String(3))

	def __repr__(self):
		return '<Course {}, Credits {}, Grade {}>'.format(self.course, self.credits, self.grade)