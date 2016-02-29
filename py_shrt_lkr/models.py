from _collections_abc import Sequence

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
from sqlalchemy.orm import relationship
from sqlalchemy.event import listen
from datetime import datetime
import time

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

from hashids import Hashids

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Hashids Generator
def hashid_generator(id):
	return Hashids(salt="I fart in your general direction!").encode(id, int(round(time.time())))


class MyModel(Base):
	__tablename__ = 'models'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	value = Column(Integer)

