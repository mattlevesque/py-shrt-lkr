import transaction

import sqlalchemy

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import (
	User
)

class UserErrors(Exception):
	pass

class UserCreationError(UserErrors):
	def __init__(self, message=None):
		self.message = message

class UserService(object):
	def __init__(self, dbsession):
		self.dbsession = dbsession

	def create(self, screenName=None, email=None, firstName=None, lastName=None, password=None):
		#Check if we already have an account
		exist=self.dbsession.query(User)\
			.filter(or_(User.screeName==screenName, User.email==email)).exists()
		if(self.dbsession.query(exist).scalar()):
			raise UserCreationError("User already exists")

		user=User()
		user.screeName=screenName
		user.email=email
		user.firstName=firstName
		user.lastName=lastName
		user.password=password


		self.dbsession.add(user)
		self.dbsession.merge(user)

		return user

	def update(self, id, screenName=None, email=None, firstName=None, lastName=None, password=None):
		with transaction.manager:
			user = self.getById(id).first()
			if user!=None:
				user.screeName=screenName
				user.email=email
				user.firstName = firstName
				user.lastName = lastName
				user.password = password
				transaction.commit()
				return 0
		return 1

	def delete(self, user = None):
		if user != None:
			with transaction.manager:
				self.dbsession.delete(user)
				transaction.commit()
		return 1

	def getById(self, id = None):
		q=self.dbsession.query(User).filter(User.id == id)
		return q.first()
	def validateLogin(self, screenName = None, password = None):
		q=self.dbsession.query(User).filter(User.screeName==screenName, User.password==password)
		ret=self.dbsession.query(q.exists()).scalar()
		return ret