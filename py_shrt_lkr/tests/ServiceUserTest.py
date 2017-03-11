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
			first_name = "test "+str(x)
			last_name = "ing"
			email = "test"+str(x)+"@hotmail.com"
			scree_name = "testing user "+str(x)
			password = "TTT"

			try:
				ret = self.user_srv.create(scree_name, email, first_name, last_name, password)
				print("Return : "+str(ret.id)+" "+str(ret.firstName))
			except:
				pass

		random_id=random.choice(range(0,10))
		self.assertEqual(self.user_srv.getById(random_id).firstName, "test "+str(random_id-1), "User found")

	def test_user_login(self):
		screen_name="User-passtst"
		passwd="ZeePassWordz"

		user=User()
		user.screeName=screen_name
		user.password=passwd

		self.user_srv.create(screen_name, None, None, None, passwd)
		# Validate good password
		self.assertEqual(self.user_srv.validateLogin(screen_name, passwd), True, "Login successful")
		# Validate bad password
		self.assertEqual(self.user_srv.validateLogin(screen_name, "Wrong PASS"), False, "Login fail pass success")