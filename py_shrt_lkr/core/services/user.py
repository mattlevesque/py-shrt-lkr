import transaction

import sqlalchemy

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import (
	User
)

#
import re

REGEX_EMAIL = re.compile(r"[^@]+@[^@]+\.[^@]+")


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

	def create(self, screen_name=None, email=None, first_name=None, last_name=None, password=None):
		# Basic validation
		if email is None or len(email) < 5 or not REGEX_EMAIL.match(email):
			raise UserCreationError("Invalid email")

		# Check if we already have an account
		exist=self.dbsession.query(User)\
			.filter(or_(User.screeName == screen_name, User.email == email)).exists()
		if self.dbsession.query(exist).scalar():
			raise UserCreationError("User already exists")

		user=User()
		user.screeName=screen_name
		user.email=email
		user.firstName=first_name
		user.lastName=last_name
		user.password=password

		self.dbsession.add(user)
		self.dbsession.merge(user)

		return user

	def update(self, id, screen_name=None, email=None, first_name=None, last_name=None, password=None):
		user = self.get_by_id(id).first()
		if user is None:
			raise UserNotFount()

		with transaction.manager:
			user.screeName=screen_name
			user.email=email
			user.firstName = first_name
			user.lastName = last_name
			user.password = password
			transaction.commit()
			return user

	def delete(self, id):
		user=self.get_by_id(id)
		if user is None:
			raise UserNotFount()

		self.dbsession.delete(user)
		self.dbsession.commit()

	def get_by_id(self, id=None):
		return self.dbsession.query(User)\
			.filter(User.id == id).first()

	def validate_login(self, screen_name=None, password=None):
		qry=self.dbsession.query(User)\
			.filter(User.screeName == screen_name, User.password == password)
		return self.dbsession.query(qry.exists()).scalar()