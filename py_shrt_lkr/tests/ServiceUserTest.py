import unittest
import transaction

from pyramid import testing

from ..core.models import Base, DBSession, User

class TestServiceUserSuccessCondition(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		from sqlalchemy import create_engine
		engine = create_engine('sqlite://')
		DBSession.configure(bind=engine)
		Base.metadata.create_all(engine)

		from ..core.services import UserService

		self.user_srv = UserService(DBSession)

	def tearDown(self):
		DBSession.remove()
		testing.tearDown()

	def test_create_user(self):


		for x in range(0,10):
			user = User()
			user.firstName = "test "+str(x)
			user.lastName = "ing"
			user.email = "test@hotmail.com"
			user.screeName = "testing user"

			ret = self.user_srv.create(user)

			print("Return : "+str(ret.id)+" "+str(ret.firstName))
		self.assertEqual(self.user_srv.getById(77), -10, "Yup that works")