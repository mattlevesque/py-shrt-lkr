import unittest
import transaction
import random

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
			firstName = "test "+str(x)
			lastName = "ing"
			email = "test"+str(x)+"@hotmail.com"
			screeName = "testing user "+str(x)
			password = "TTT"

			try:
				ret = self.user_srv.create(screeName, email, firstName, lastName, password)
				print("Return : "+str(ret.id)+" "+str(ret.firstName))
			except:
				pass


		x = self.user_srv.getById(7);
		randomId=random.choice(range(0,10))
		self.assertEqual(self.user_srv.getById(randomId).firstName, "test "+str(randomId-1), "User found")
	def test_user_login(self):
		screenname="User-passtst"
		passwd="ZeePassWordz"

		user=User()
		user.screeName=screenname
		user.password=passwd

		self.user_srv.create(screenname, None, None, None, passwd)
		# Validate good password
		self.assertEqual(self.user_srv.validateLogin(screenname, passwd), True, "Login successful")
		# Validate bad password
		self.assertEqual(self.user_srv.validateLogin(screenname, "Wrong PASS"), False, "Login fail pass success")