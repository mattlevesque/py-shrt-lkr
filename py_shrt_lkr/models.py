from _collections_abc import Sequence
from sqlalchemy import (
	Column,
	Index,
	Integer,
	Text,
	Sequence,
	String,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
	__tablename__ = 'models'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	value = Column(Integer)


Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Link(Base):
	__tablename__ = 'link'
	#id = Column(Integer, Sequence('link_id_seq'), primary_key=True)
	id = Column(Integer, primary_key=True)
	description = Column(String(75))
	shorty = Column(String(128))
	url = Column(String(512))

Index('link_shorty_index', Link.shorty, unique=True, mysql_length=255)