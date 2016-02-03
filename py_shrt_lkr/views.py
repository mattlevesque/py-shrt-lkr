import re
import sqlalchemy
import colander
import deform.widget
import transaction
import time
from pyramid.httpexceptions import HTTPFound
from hashids import Hashids

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from sqlalchemy import Sequence

from .models import (
	DBSession,
	MyModel,
	Link,
)


@view_config(route_name='home', renderer='templates/mytemplate.mako')
def my_view(request):
	try:
		one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
	except DBAPIError:
		return Response(conn_err_msg, content_type='text/plain', status_int=500)
	return {'one': one, 'project': 'py-shrt-lkr'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_py-shrt-lkr_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

# http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/forms.html

# matches an IP, localhost or a domain
expr_url = re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", re.IGNORECASE)

class ShortLink(colander.MappingSchema):
	description = \
		colander.SchemaNode(
			colander.String(),
			validator=colander.Length(min=3, max=50, min_err=u'Shorter than minimum length of ${min}', max_err=u'Longer than maximum length ${max}'),)
	url = colander.SchemaNode(
			colander.String(),
			default="http://",
			title=u'Url',
			validator=colander.Regex(
				expr_url,
				msg=u"Not valid URL"
			))


class ShortLinkEdit(ShortLink):
	short = colander.SchemaNode(
			colander.String(),
			title=u'Short'
		)


from sqlalchemy.orm.exc import NoResultFound

class LinkViews(object):
	def __init__(self, request):
		self.request = request
		self.hash_gen = Hashids(salt="I fart in your general direction!")

	@property
	def link_form(self, schema=ShortLink()):
		#schema = ShortLink()
		return deform.Form(schema, buttons=('submit',))

	@property
	def reqts(self):
		return self.link_form.get_widget_resources()

	@view_config(route_name='link_hit')
	def hit(self):
		print(self.request.path)
		pathSplit = str.split(self.request.path, sep="/")
		if(len(pathSplit) > 1):
			short=pathSplit[1]

			try:
				link = DBSession.query(Link).filter_by(shorty=short).one()
				print("It's a hit!")
				return Response(status=302, location=link.url)
			except NoResultFound:
				print('No link found...')

		return Response("No hit... (Sorry)")

	@view_config(route_name='link_list', renderer='templates/link/list.mako')
	def list(self):
		linksLst = DBSession.query(Link)

		return {'linkLst': linksLst}

	@view_config(route_name='link_create', renderer='templates/link/create.mako')
	def create(self):
		print('link:create')
		form = self.link_form.render()

		print (self.request.params)
		print('submit' in self.request.POST)

		data = self.request.POST
		if 'submit' in data:
			controls = data.items()
			try:
				print('try')
				appstruct = self.link_form.validate(controls)
			except deform.ValidationFailure as e:
				print('except')
				return {'test': '<h5>Bad entry... RETRY!!!</h5>', 'form': e.render()}
			#Save the data
			model = Link()
			model.description = data['description']
			model.url = data['url']

			with transaction.manager as trans:
				maxId=DBSession.execute(sqlalchemy.func.max(Link.id)).first()[0]
				if maxId is None:
					maxId=0
				nextId = maxId+1
				hashid = self.hash_gen.encode(nextId, int(round(time.time())))

				model.shorty = hashid
				DBSession.add(model)
				trans.commit()
			print(self.request.POST['url'])

			#return HTTPFound(self.request.route_url('link_list'))
		return {'test': '<h5>TEST</h5>', 'form': form}

	@view_config(route_name='link_edit', renderer='templates/link/edit.mako')
	def edit(self):
		id = self.request.matchdict.get('id', None)

		link = DBSession.query(Link).filter_by(id=id).one()

		schema = ShortLinkEdit()

		form = deform.Form(schema, buttons=('submit',))

		data = self.request.POST
		if 'submit' in data:
			controls = data.items()
			try:
				print('try')
				self.link_form.validate(controls)

				#Save the data
				link.description = data['description']
				link.url = data['url']
				transaction.commit()
				#Refreshing the model
				link = DBSession.query(Link).filter_by(id=id).one()

			except deform.ValidationFailure as e:
				print('except')
				return {'data': '<h5>Bad entry... RETRY!!!</h5>', 'id': id, 'form': e.render()}

		return {'data': "TEST", 'id': id, 'form':form.render({'id':link.id, 'description': link.description, 'url':link.url, 'shorty': ''})}
	@view_config(route_name='link_delete')
	def delete(self):
		id = self.request.matchdict.get('id', None)
		link = DBSession.query(Link).filter_by(id=id).one()

		DBSession.delete(link)
		transaction.commit()

		return Response(status=302, location=self.request.route_url("link_list"))