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


class Tag(Base):
	__tablename__ = 'tag'
	id = Column(Integer, Sequence('tag_id_seq'), primary_key=True)
	name = Column(String(64))
Index('tag_name_index', Tag.name, unique=True, mysql_length=255)


