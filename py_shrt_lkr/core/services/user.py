import transaction

import sqlalchemy

from sqlalchemy.orm.exc import NoResultFound

from ..models.user import (
	User
)

class UserService(object):
	def __init__(self, dbsession):
		self.dbsession = dbsession

	def create(self, user = None):

		self.dbsession.add(user)
		self.dbsession.merge(user)

		return user

	def update(self, user = None):
		with transaction.manager:
			user = self.getById( user.id )

		return -1

	def delete(self, user = None):
		return -1

	def getById(self, id = None):
		qry = self.dbsession.query(User).filter(User.id==id)
		return qry.first()