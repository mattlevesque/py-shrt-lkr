import transaction

import sqlalchemy

from sqlalchemy.orm.exc import NoResultFound

from ..models.links import (
	Link,
	LinkHit,
)

from ..models.taxonomy import (
	Tag
)

from py_shrt_lkr.helpers import (
	list_diff
)

class LinkService(object):
	def __init__(self, dbsession):
		self.dbsession = dbsession
	def create_link(self, url, title=None, description=None):
		link = Link(url=url, title=title, description=description)

		with transaction.manager:
			self.dbsession.add(link)
			transaction.commit()
			created_id = self.dbsession.execute(sqlalchemy.func.max(Link.id)).first()[0]
		return created_id

	def edit_link(self, id, name=None, title=None, description=None, shorty=None, url=None, tags=None):
		with transaction.manager:
			link = self.get_link_by_id(id)
			link.title = title
			link.description = description
			link.shorty = shorty
			link.url = url

			currentTagLst = list(map(lambda x: x.name, link.tags))

			formTags = tags.split(',')
			newTags = list_diff(currentTagLst, formTags)
			deletedTags = list_diff(formTags, currentTagLst)

			#print("Tags : "+tags)
			#print("Cur : "+str(currentTagLst))
			#print("New : "+str(newTags))
			#print("Del : "+str(deletedTags))

			#Delete the removed tags
			if len(deletedTags)>0:
				delIndx=list(map(lambda x: currentTagLst.index(x), deletedTags))
				delIndx.sort()
				delIndx.reverse()
				print("Del indx "+str(delIndx))
				for indx in delIndx:
					print("Remove indx : %d"%indx)
					link.tags.pop(indx)

			#Insert the new tags
			if len(newTags)>0:
				for tagName in newTags:
					tag = None
					try:
						tag=self.dbsession.query(Tag).filter_by(name=tagName).one()
					except NoResultFound:
						#If not found we create it
						tag=Tag(name=tagName)
					link.tags.append(tag)

			transaction.commit()

	def get_link_by_id(self, id):
		try:
			return self.dbsession.query(Link).filter_by(id=id).one()
		except NoResultFound:
			return None;

	def delete_link(self, id):
		if id != None:
			link = self.get_link_by_id(id)

			if link != None:
				self.dbsession.delete(link)
				transaction.commit()

