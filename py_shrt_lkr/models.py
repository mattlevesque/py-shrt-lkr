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


Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Link(Base):
	__tablename__ = 'link'
	#id = Column(Integer, Sequence('link_id_seq'), primary_key=True)
	id = Column(Integer, primary_key=True)
	title = Column(String(75))
	description = Column(String(512))
	shorty = Column(String(128))
	url = Column(String(512))
	hits = relationship("LinkHit", back_populates="link")

	def hitCount(self):
		return len(self.hits)

Index('link_shorty_index', Link.shorty, unique=True, mysql_length=255)

# Links events

def generate_shorty(mapper, connect, target):
	if target.shorty is None or target.shorty == "":
		id = target.id
		if id is None:
			maxId=connect.execute(sqlalchemy.func.max(Link.id)).first()[0]
			if maxId is None:
				maxId=0
			id = maxId+1
		target.shorty = hashid_generator(id)

listen(Link, 'before_insert', generate_shorty)
listen(Link, 'before_update', generate_shorty)

class LinkHit(Base):
	__tablename__ = 'link_hit'
	id = Column(Integer, Sequence('link_hit_id_seq'), primary_key=True)
	link_id = Column(Integer, ForeignKey('link.id'))
	link = relationship("Link", back_populates="hits")
	date_stamp = Column(DateTime, default=datetime.now())
	referer = Column(String(1024))
