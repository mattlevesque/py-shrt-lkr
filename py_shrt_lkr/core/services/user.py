import transaction

import sqlalchemy

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import (
	User
)

class UserErrors(Exception):
	pass

class UserNotFount(Exception):
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
		user = self.getById(id).first()
		if user is None:
			raise UserNotFount()

		with transaction.manager:
			user.screeName=screenName
			user.email=email
			user.firstName = firstName
			user.lastName = lastName
			user.password = password
			transaction.commit()
			return user

	def delete(self, id):
		user=self.getById(id)
		if user is None:
			raise UserNotFount()

		self.dbsession.delete(user)
		self.dbsession.commit()

	def getById(self, id=None):
		return self.dbsession.query(User)\
			.filter(User.id == id).first()

	def validateLogin(self, screenName=None, password=None):
		qry=self.dbsession.query(User)\
			.filter(User.screeName == screenName, User.password == password)
		return self.dbsession.query(qry.exists()).scalar()
