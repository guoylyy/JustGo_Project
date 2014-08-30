import os 
import random
import json
import csv
import simplejson as json
from datetime import datetime,timedelta
from flask import Flask, request, flash, url_for, redirect, \
	 render_template, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import or_
from sqlalchemy import Table 
from flask.ext import restful
from flask.ext.restful import reqparse


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers')

#============== Decorators =============#

#=============  End Decorators =========#


#============= UDF ==================#
def abort_if_category_doesnt_exist(category_name):
	if Category.query.filter(Category.category_name==category_name).count() == 0:
		restful.abort(404, message="Category {} doesn't exist".format(category_name))

def abort_if_user_doesnt_exit(user_id):
	if User.query.filter(User.user_id==user_id).count() == 0:
		restful.abort(404, message="User with ID {} doesn't exist".format(user_id))
	else:
		return 	User.query.filter(User.user_id==user_id).first()

def check_authorization():
	token = parser.parse_args()['Authorization']
	#TO-DO: Check token exipred and invalid
	if not token:
		restful.abort(500, message="Authorization Failed")
	else:
		# Check expired
		return User.query.filter(User.token==token).first()

#============= End of UDF ===========#


#============== APIs =============#
class GoalCategoryRest(restful.Resource):
	def get(self):
		l = Category.query.all()
		return [c.to_json() for c in l], 200

class GoalRest(restful.Resource):
	# TO-DO: Add people number to each category
	def get(self, category_id):
		abort_if_category_doesnt_exist(category_id)
		c = Category.query.filter(Category.category_name==category_id).first()
		goals = c.goals
		return [g.to_json() for g in goals] ,200

	def __goal_details(self, goal_id):
		return ""

class UserRest(restful.Resource):
	def get(self, user_id):
		user = abort_if_user_doesnt_exit(user_id)
		return user.to_json(), 200

	def post(self):
		#check_authorization()
		up = self.__user_parser()
		user = User.query.filter(User.facebook_token==up['facebook_token']).first()
		if user is None:
			#register
			token = "fdsafsafas"
			u = User(up['name'],up['description'],token,up['facebook_token'],'header')	
			db.session.add(u)
			flag = db.session.commit()
			return {'token': u.token}, 204
		else:
			return {'token': user.token}, 200

	def __user_parser(self):
		up = reqparse.RequestParser()
		up.add_argument('facebook_token', type=str, location='form')
		up.add_argument('name', type=str, location='form')
		up.add_argument('description', type=str, location='form')
		return up.parse_args()

class GoalRecordRest(restful.Resource):
	def get(self, record_id):
		g = GoalRecord.query.filter(GoalRecord.goal_record_id==record_id).first()
		if g:
			return g.to_json(), 200
		else:
			restful.abort(404, 'Goal Record with ID {} does exist.'.format(record_id))

	def post(self):
		""" Add a record for specific goal
		"""
		user = check_authorization()
		up = self.__record_parser()
		g = GoalRecord(up['goal_id'], user.user_id, up['content'], 'fdsafa')
		db.session.add(g)
		flag = db.session.commit()
		return {'result':'success'}, 200

	def __record_parser(self):
		up = reqparse.RequestParser()
		up.add_argument('content', type=str, location='form')
		up.add_argument('goal_id', type=int, location='form')
		return up.parse_args()


class GoalRecordCommentRest(restful.Resource):
	def get(self, record_id):
		""" Get all comments of a goal_record
		"""
		gr = GoalRecord.query.filter(GoalRecord.goal_record_id==record_id).first()
		return [grc.to_json() for grc in gr.comments.all()], 200

	def post(self, record_id):
		""" Add a comment to specific goal_record
		"""
		user = check_authorization()
		up = self.__comment_parser()
		grc = GoalRecordComment(record_id, user.user_id, up['content'])
		db.session.add(grc)
		flag = db.session.commit()
		return {'result' : flag}, 200

	def __comment_parser(self):
		up = reqparse.RequestParser()
		up.add_argument('content', type=str, location='form')
		return up.parse_args()		


class GoalRecordAwesomeRest(restful.Resource):
	"""docstring for GoalRecordAwesomeRest"""
	def get(self, record_id):
		gr = GoalRecord.query.filter(GoalRecord.goal_record_id==record_id).first()
		return [gra.to_json() for gra in gr.awesomes.all()], 200

	def post(self, record_id):
		user = check_authorization()
		gra = GoalRecordAwesome(record_id, user.user_id)
		db.session.add(gra)
		db.session.commit()
		return {'result':'success'}, 200
		

#============== End of APIs =============#


#============== Routes ============#
api.add_resource(UserRest, '/'+ app.config['VERSION'] + '/user/<string:user_id>','/'+ app.config['VERSION'] + '/user')

api.add_resource(GoalCategoryRest, '/'+ app.config['VERSION'] + '/goal_category')
api.add_resource(GoalRest, '/'+ app.config['VERSION'] + '/goal/<string:category_id>')
api.add_resource(GoalRecordRest, '/'+ app.config['VERSION'] + '/goal_record/<int:record_id>','/'+ app.config['VERSION'] + '/goal_record')
api.add_resource(GoalRecordCommentRest, '/'+ app.config['VERSION'] + '/goal_record_comment/<int:record_id>')
api.add_resource(GoalRecordAwesomeRest, '/'+ app.config['VERSION'] + '/goal_record_awesome/<int:record_id>')


#============== End of Routes =====#

#================== Models =====================#

class User(db.Model):
	__tablename__ = "user"
	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	token = db.Column(db.String)
	facebook_token = db.Column(db.String)
	header_icon = db.Column(db.String)

	def __init__(self, name, description, token, facebook_token, header_icon):
		self.name = name
		self.description = description
		self.token = token
		self.facebook_token = facebook_token
		self.header_icon = header_icon
		self.update_time = datetime.now()

	def to_json(self):
		return {
			'user_id' : self.user_id,
			'name' : self.name,
			'description': self.description
		}

user_follow = db.Table('user_follow',
	db.Column('follow_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

goal_category = db.Table('goal_category',
	db.Column('goal_id', db.Integer, db.ForeignKey('goal.goal_id')),
	db.Column('category_name', db.String , db.ForeignKey('category.category_name'))
)

class Category(db.Model):
	"""docstring for GoalCategory"""
	__tablename__ = "category"
	category_name = db.Column(db.String, primary_key=True)
	desciprtion = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	goals = db.relationship('Goal', secondary=goal_category, backref=db.backref('categorys', lazy='dynamic'))

	def __init__(self, category_name, update_time, desciprtion):
		self.category_name = category_name
		self.desciprtion = desciprtion
		self.update_time = update_time

	def to_json(self):
		return {
			'category_name' : self.category_name,
			'desciprtion' : self.desciprtion
		}

class Goal(db.Model):
	""" Goal table is only write in server """
	__tablename__ = "goal"
	goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	goal_name = db.Column(db.String, unique=True)
	image = db.Column(db.String)
	desciprtion = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	#goal_joins = db.relationship('goal_join', lazy='dynamic')

	def to_json(self):
		return {
			'goal_id' : self.goal_id,
			'goal_name' : self.goal_name,
			'desciprtion' : self.desciprtion
		}
	
class GoalJoin(db.Model):
	__tablename__ = "goal_join"
	goal_join_id = db.Column(db.String, primary_key=True)
	goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
	user_id = db.Column(db.Integer)
	time_span = db.Column(db.Integer)
	frequency = db.Column(db.String)
	is_reminder = db.Column(db.Boolean)
	reminder_time = db.Column(db.Time)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	is_finished = db.Column(db.Boolean)
	update_time = db.Column(db.DateTime)

	#goal_tracks = db.relationship('goal_track', lazy='dynamic')


class GoalTrack(db.Model):
	""" Track everydays' status of a goal for one user """
	__tablename__ = "goal_track"
	goal_track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	goal_join_id = db.Column(db.Integer, db.ForeignKey('goal_join.goal_join_id'))
	track_date = db.Column(db.DateTime)
	update_time = db.Column(db.DateTime)


class GoalRecord(db.Model):
	""" Records for a specific goal """
	__tablename__ = 'goal_record'
	goal_record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	goal_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	content = db.Column(db.String)
	image = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	comments = db.relationship('GoalRecordComment', backref='goal_record', lazy='dynamic')
	awesomes = db.relationship('GoalRecordAwesome', backref='goal_record', lazy='dynamic')

	def __init__(self, goal_id, user_id, content, image):
		self.goal_id = goal_id
		self.user_id = user_id
		self.content = content
		self.image = image

	def to_json(self):
		return {
			'goal_record_id': self.goal_record_id,
			'goal_id' : self.goal_id,
			'content' : self.content,
			'image' : self.image
		}

class GoalRecordComment(db.Model):
	"""docstring for GoalRecordComment"""
	__tablename__ = 'goal_record_comment'
	comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	goal_record_id = db.Column(db.Integer, db.ForeignKey('goal_record.goal_record_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	content = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)

	def __init__(self, goal_record_id, user_id, content):
		self.goal_record_id = goal_record_id
		self.user_id = user_id
		self.content = content
		self.update_time = datetime.now()
		self.create_time = datetime.now()

	def to_json(self):
		return {
			'comment_id' : self.comment_id,
			'goal_record_id' : self.goal_record_id,
			'user_id' : self.user_id,
			'content' : self.content,
			'create_time' : self.create_time
		}


class GoalRecordAwesome(db.Model):
	"""docstring for GoalRecordAwesome"""
	__tablename__ = 'goal_record_awesome'
	awesome_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	goal_record_id = db.Column(db.Integer, db.ForeignKey('goal_record.goal_record_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)
	
	def __init__(self, goal_record_id, user_id):
		self.goal_record_id = goal_record_id
		self.user_id = user_id
		self.create_time = datetime.now()
		self.update_time = datetime.now()

	def to_json(self):
		return {
			'awesome_id' : self.awesome_id,
			'goal_record_id' : self.goal_record_id,
			'user_id' : self.user_id
		}

class Notification(db.Model):
	"""docstring for Notification"""
	__tablename__ = 'notification'
	notificaion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	notificaion_type = db.Column(db.String)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	content = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)
	is_readed = db.Column(db.Boolean, default=False)
	
	def __init__(self, notificaion_type, sender_id, receiver_id, content):
		self.notificaion_type = notificaion_type
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		self.content = content
		self.update_time = self.create_time = datetime.now()

	def to_json(self):
		return {
			'notificaion_id' : self.notificaion_id,
			'user_id' : self.user_id,
			'content' : self.content
		}

#============== End of Models ============================#
		
def init_db():
	db.drop_all()
	db.create_all()
	make_wp_data()

def update_db():
	db.update()

def make_wp_data():
	categories = ['Popular', 'Health Diet', 'Train plans', 'Habits', 'Learning']
	for cat in categories:
		db.session.add(Category(cat, datetime.now(), ''))
	db.session.commit()

def _test_categories():
	c = Category.query.filter(Category.category_name=='Popular').count()
	print c

def make_goal_data():
	pass


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
#================= APIs ========================#
