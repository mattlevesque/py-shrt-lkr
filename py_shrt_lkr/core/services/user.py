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
		return -1

	def update(self, user = None):
		with transaction.manager:
			user = self.getById( user.id )

		return -1

	def delete(self, user = None):
		return -1

	def getById(self, id = None):
		return -1