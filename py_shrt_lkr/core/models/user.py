import sqlalchemy
from sqlalchemy import (
	Column,
	DateTime,
	ForeignKey,
	Index,
	Integer,
	Text,
	Sequence,
	String,
	Table,
)

from .base import (
	Base,
	DBSession,
)

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	screeName = Column(String(75))
	firstName = Column(String(128))
	lastName = Column(String(128))
	email = Column(String(256))
	password = Column(String(256))
