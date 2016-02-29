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

from .base import (
	Base,
	DBSession,
)

from .taxonomy import Tag


from hashids import Hashids


# Hashids Generator
def hashid_generator(id):
	return Hashids(salt="I fart in your general direction!").encode(id, int(round(time.time())))

link_tag_association_table = Table('link_tag', Base.metadata,
	Column('link_id', Integer, ForeignKey('link.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Link(Base):
	__tablename__ = 'link'
	#id = Column(Integer, Sequence('link_id_seq'), primary_key=True)
	id = Column(Integer, primary_key=True)
	title = Column(String(75))
	description = Column(String(512))
	shorty = Column(String(128))
	url = Column(String(512))
	hits = relationship("LinkHit", back_populates="link")
	tags = relationship(
		"Tag",
		secondary=link_tag_association_table
	)

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


