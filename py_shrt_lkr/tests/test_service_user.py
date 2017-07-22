import unittest
import transaction
import random

from pyramid import testing

from py_shrt_lkr.core.models import Base, DBSession, User
from py_shrt_lkr.core.services import UserService

class TestServiceUserSuccessCondition(unittest.TestCase):
	USER_TEST_COUNT = 10
	def setUp(self):
		print("Setup...")
		self.config = testing.setUp()
		from sqlalchemy import create_engine
		engine = create_engine('sqlite://')
		DBSession.configure(bind=engine)
		Base.metadata.create_all(engine)

		self.dbsession = DBSession


		self.user_srv = UserService(self.dbsession)

		# Create users
		for x in range(0,self.USER_TEST_COUNT):
			user = User()
			user.firstName = "test "+str(x)
			user.lastName = "ing"
			user.email = "test@hotmail.com"
			user.screeName = "testing user"

			ret = self.user_srv.create(user)

			print("Return : "+str(ret.id)+" "+str(ret.firstName))

	def tearDown(self):
		print("TearDown...")
		self.dbsession.remove()
		testing.tearDown()

	def getRandomUSer(self):
		nbr_rand = random.randint(1, self.USER_TEST_COUNT)
		user = self.user_srv.getById(nbr_rand)
		return {
			"user": user,
			"nbr": nbr_rand
		}

	def test_create_user(self):
		user = self.getRandomUSer()



		self.assertIsNotNone(user["user"], "The random user wasn't found")

	def test_update_user(self):
		usr_stk = []
		#Get the users
		for z in self.dbsession.query(User).all():
			usr_stk.insert(0, z)
		#Update them all
		cnt=0
		for z in usr_stk:
			z.firstName = "Updated "+str(cnt)
			print(z.firstName+" "+z.lastName)
			self.user_srv.update(z)
			cnt+=1

		self.user_srv.getById(random.randint(1, self.USER_TEST_COUNT))



		self.assertEqual(self.user_srv.getById(77), -10, "Yup that works")
		return 0