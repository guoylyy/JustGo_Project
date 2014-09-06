# -*- coding: utf-8 -*-
import time as stime

from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import or_
from sqlalchemy import Table 
from datetime import datetime, timedelta, time , date
from extensions import db, fs_store
from sqlalchemy_imageattach.entity import Image, image_attachment, store_context
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore, FileSystemStore
from app.helpers import _str2date, _find_or_create_thumbnail, _mk_timestamp


#================== Models =====================#
user_follow = db.Table('user_follow',
	db.Column('follow_id', db.Integer, db.ForeignKey('user.user_id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

class User(db.Model):
	__tablename__ = "user"
	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	token = db.Column(db.String)
	facebook_token = db.Column(db.String)
	header_icon = image_attachment('UserHeader')
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)

	followings = db.relationship('User', secondary=user_follow, primaryjoin=user_id==user_follow.c.follow_id, \
		secondaryjoin=user_id==user_follow.c.followed_id,backref=db.backref('u_fans', lazy='dynamic'))
	
	fans = db.relationship('User', secondary=user_follow, primaryjoin=user_id==user_follow.c.followed_id, \
		secondaryjoin=user_id==user_follow.c.follow_id,backref=db.backref('u_followings', lazy='dynamic'))

	def __init__(self, name, description, token, facebook_token, header_icon):
		self.name = name
		self.description = description
		self.token = token
		self.facebook_token = facebook_token
		self.update_time = datetime.now()
		self.create_time = datetime.now()

	def header_json(self):
		return {
			'user_id' : self.user_id,
			'header' : _find_or_create_thumbnail(self, self.header_icon,48).locate(),
			'user_name' : self.name
		}

	def to_json(self):
		with store_context(fs_store):
			return {
				'user_id' : self.user_id,
				'name' : self.name,
				'description': self.description,
				'fans' : [f.header_json() for f in self.fans],
				'followings' : [fo.header_json() for fo in self.followings],
				'can_follow' : True,
				'header_icon' : _find_or_create_thumbnail(self, self.header_icon,48).locate()
			}

class UserHeader(db.Model, Image):
	__tablename__ = 'user_header'
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
	user = db.relationship('User')


goal_category = db.Table('goal_category',
	db.Column('goal_id', db.Integer, db.ForeignKey('goal.goal_id')),
	db.Column('category_name', db.String , db.ForeignKey('category.category_name'))
)

class Category(db.Model):
	""" GoalCategory
	"""
	__tablename__ = "category"
	category_name = db.Column(db.String, primary_key=True)
	desciprtion = db.Column(db.String)
	create_time = db.Column(db.DateTime)
	update_time = db.Column(db.DateTime)
	goals = db.relationship('Goal', secondary=goal_category, backref=db.backref('categorys', lazy='dynamic'))

	def __init__(self, category_name, update_time, desciprtion):
		self.category_name = category_name
		self.desciprtion = desciprtion
		self.update_time = update_time
		self.create_time = datetime.now()

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
	image = image_attachment('GoalImage')
	desciprtion = db.Column(db.String)
	create_time = db.Column(db.DateTime)
	update_time = db.Column(db.DateTime)
	goal_joins = db.relationship('GoalJoin', backref='goal', lazy='dynamic')

	def __init__(self, goal_name, description):
		self.goal_name = goal_name
		self.description = description
		self.create_time = datetime.now()
		self.update_time = datetime.now()

	def to_json(self):
		with store_context(fs_store):
			return {
				'goal_id' : self.goal_id,
				'goal_name' : self.goal_name,
				'desciprtion' : self.desciprtion,
				'joins' : self.goal_joins.count(),
				'image' : self.image.locate(),
				'joins' : self.goal_joins.count()

			}

class GoalImage(db.Model, Image):
	__tablename__ = 'goal_image'
	user_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), primary_key=True)
	user = db.relationship('Goal')

class GoalJoin(db.Model):
	__tablename__ = "goal_join"
	goal_join_id = db.Column(db.String, primary_key=True)
	goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	time_span = db.Column(db.Integer)
	frequency = db.Column(db.String)
	is_reminder = db.Column(db.Boolean)
	reminder_time = db.Column(db.Time)
	start_date = db.Column(db.Date)
	end_date = db.Column(db.Date)
	is_finished = db.Column(db.Boolean, default=False)
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)
	
	def __init__(self, *args , **kwargs):
		if args:
			self.goal_join_id = args[0]
			self.goal_id = args[1]
			self.user_id = args[2]
			self.time_span = args[3]
			self.frequency = args[4]
			self.is_reminder = args[5]
			self.reminder_time = args[6]
			self.start_date = args[7]
			self.end_date = args[8]
			self.is_finished = args[9]
			self.update_time = self.create_time = datetime.now()
		else:
			self.goal_join_id = kwargs['goal_join_id']
			self.__receive_from_json(kwargs)


	def update_from_json(self, **kwargs):
		self.__receive_from_json(kwargs)

	def __receive_from_json(self, kwargs):
		self.goal_id = kwargs['goal_id']
		self.user_id = kwargs['user_id']
		self.time_span = kwargs['time_span']
		self.frequency = kwargs['frequency']
		self.is_reminder = kwargs['is_reminder']
		self.reminder_time = _str2time(kwargs['reminder_time'])
		self.start_date = _str2date(kwargs['start_date'])
		self.end_date = _str2date(kwargs['end_date'])
		self.is_finished = kwargs['is_finished']
		self.update_time = datetime.now()
		self.create_time = datetime.fromtimestamp(kwargs['create_time'])

	def to_json(self):
		return {
			'goal_join_id' : self.goal_join_id,
			'goal_id' : self.goal_id,
			'user_id' : self.user_id,
			'time_span': self.time_span,
			'frequency' : self.frequency,
			'is_reminder' : self.is_reminder,
			'reminder_time' : self.reminder_time.isoformat(),
			'start_date' : self.start_date.isoformat(),
			'end_date' : self.end_date.isoformat(),
			'is_finished': self.is_finished,
			'update_time' : _mk_timestamp(self.update_time),
			'create_time' : _mk_timestamp(self.create_time)
		}

	def __get_goal(self):
		return Goal.query.filter(Goal.goal_id==self.goal_id).first()

	goal = property(__get_goal)

class GoalTrack(db.Model):
	""" Track everydays' status of a goal for one user """
	__tablename__ = "goal_track"
	goal_track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	goal_join_id = db.Column(db.Integer, db.ForeignKey('goal_join.goal_join_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	track_date = db.Column(db.Date)
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)

	def __init__(self, *args, **kwargs):
		if args:
			self.goal_join_id = args[0]
			self.user_id = args[1]
			self.track_date = args[2]
			self.update_time = self.create_time = datetime.now()
		else:
			self.__receive_from_json(kwargs)

	def update_from_json(self, **kwargs):
		self.__receive_from_json(kwargs)

	def __receive_from_json(self, kwargs):
		self.goal_join_id = kwargs['goal_join_id']
		self.user_id = kwargs['user_id']
		self.track_date = _str2date(kwargs['track_date'])
		self.update_time = datetime.now()

	def to_json(self):
		return {
			'goal_track_id' : self.goal_track_id,
			'goal_join_id' : self.goal_join_id,
			'user_id' : self.user_id,
			'track_date' : self.track_date.isoformat(),
			'update_time' : _mk_timestamp(self.update_time),
			'create_time' : _mk_timestamp(self.create_time)
		}

class GoalRecord(db.Model):
	""" Records for a specific goal """
	__tablename__ = 'goal_record'
	goal_record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	content = db.Column(db.String)
	image = image_attachment('GoalRecordImage')
	create_time = db.Column(db.DateTime)
	update_time = db.Column(db.DateTime)
	comments = db.relationship('GoalRecordComment', backref='goal_record', lazy='dynamic')
	awesomes = db.relationship('GoalRecordAwesome', backref='goal_record', lazy='dynamic')

	def __init__(self, goal_id, user_id, content):
		self.goal_id = goal_id
		self.user_id = user_id
		self.content = content
		self.update_time = datetime.now()
		self.create_time = datetime.now()

	def __can_awesome(self, user):
		if (user.user_id == self.user_id) or (user.user_id in [ga.user_id for ga in self.awesomes.all()]):
			return False
		else:
			return True

	def to_json(self, user):
		with store_context(fs_store):
			return {
				'goal_record_id': self.goal_record_id,
				'goal_id' : self.goal_id,
				'content' : self.content,
				'image' : self.image.locate(),
				'comments' : [c.to_json() for c in self.comments.all()],
				'awesomes' : [a.to_json() for a in self.awesomes.all()],
				'can_awesome' : self.__can_awesome(user)
			}


class GoalRecordImage(db.Model, Image):
	""" Image with sqlalchemy_imageattach
	"""
	__tablename__ = 'goal_record_image'
	goal_record_id = db.Column(db.Integer, db.ForeignKey('goal_record.goal_record_id'),\
		 primary_key=True)
	goal_record = relationship('GoalRecord')


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
			'create_time' : stime.mktime(self.create_time.timetuple())
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
	"""docstring for Notification
	"""
	__tablename__ = 'notification'
	notificaion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	notificaion_type = db.Column(db.String)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	content = db.Column(db.String)
	attach_key = db.Column(db.String)
	update_time = db.Column(db.DateTime)
	create_time = db.Column(db.DateTime)
	is_readed = db.Column(db.Boolean, default=False)
	
	def __init__(self, notificaion_type, sender_id, receiver_id, content, attach_key):
		self.notificaion_type = notificaion_type
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		self.content = content
		self.attach_key = str(attach_key)
		self.update_time = self.create_time = datetime.now()

	def to_json(self):
		return {
			'notificaion_id' : self.notificaion_id,
			'user_id' : self.sender_id,
			'content' : self.content
		}


#============== End of Models ============================#