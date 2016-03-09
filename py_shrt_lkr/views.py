import re
import sqlalchemy
import colander
import deform.widget
import transaction
import time
from pyramid.httpexceptions import HTTPFound
from hashids import Hashids
import lxml.html

from .helpers import (
	list_diff
)

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from sqlalchemy import Sequence


from .models import (
	DBSession,
	MyModel,
)

from .core.services import (
	LinkService
)



from .core.models import (
	Link,
	LinkHit,
	Tag
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
	#Todo: Reevaluate this!
	#The id is only used for the validation of the shorty and has to be included in the schema. The data gets
	#overwritten so that the id can not be fiddle with in the actual form. (Quick solution for now...)
	id = \
		colander.SchemaNode(
			colander.Integer(),
			widget=deform.widget.HiddenWidget(),
			missing=u''
		)
	title = \
		colander.SchemaNode(
			colander.String(),
			validator=colander.Length(min=3, max=75, min_err=u'Shorter than minimum length of ${min}', max_err=u'Longer than maximum length ${max}'),
		)
	description = \
		colander.SchemaNode(
			colander.String(),
			widget=deform.widget.TextAreaWidget(cols=20, rows=5),
			validator=colander.Length(min=3, max=512, min_err=u'Shorter than minimum length of ${min}', max_err=u'Longer than maximum length ${max}'),)
	url = colander.SchemaNode(
			colander.String(),
			default="http://",
			title=u'Url',
			validator=colander.Regex(
				expr_url,
				msg=u"Not valid URL"
			))
	tags = colander.SchemaNode(
			colander.String(),
			widget=deform.widget.TextInputWidget(css_class='tagit'),
			id='tags',
			missing=u''
			)


def full_form_validator(schema, form, value):
	qry=None
	if value['id'] is not None and value['id']!='':
		qry = DBSession\
				.query(sqlalchemy.func.count(Link.id))\
					.filter(Link.id!=value['id'])\
					.filter(Link.shorty==value['shorty'])
	else:
		qry = DBSession\
				.query(sqlalchemy.func.count(Link.id))\
					.filter(Link.id==value['id'])
	count=0
	try:
		count = DBSession.execute(qry).first()[0]
	except:
		raise colander.Invalid(form, u'An error has occured')

	if count>0:
		exc = colander.Invalid(form, u'Invalid shorty')
		exc['shorty'] = u'The shorty "'+value['shorty']+'" has already been taken'
		raise exc


class ShortLinkEdit(ShortLink):
	shorty = colander.SchemaNode(
			colander.String(),
			title=u'Shorty',
			missing=u'',
	)
	validator=full_form_validator


def build_link(request, link):
	return "http://0.0.0.0:6543/"+link.shorty


from sqlalchemy.orm.exc import NoResultFound

class LinkViews(object):
	def __init__(self, request):
		self.request = request
		self.hash_gen = Hashids(salt="I fart in your general direction!")

		self.link_service = LinkService(DBSession)

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

				linkHit = LinkHit()
				linkHit.link = link

				#Set the referer
				linkHit.referer = self.request.referer

				DBSession.add(linkHit)

				#print("It's a hit! from "+referer)
				return Response(status=302, location=link.url)
			except NoResultFound:
				print('No link found...')

		return Response("No hit... (Sorry)")

	@view_config(route_name='link_list', renderer='templates/link/list.mako')
	def list(self):
		linksLst = DBSession.query(Link)

		class QuickCreateShortLink(colander.MappingSchema):
			url = colander.SchemaNode(
			colander.String(),
			default="http://",
			title=u'Url',
			validator=colander.Regex(
				expr_url,
				msg=u"Not valid URL"
			))

		quick_create_frm = deform.Form(QuickCreateShortLink(), buttons=('submit',))

		data = self.request.POST

		quick_create_frm_rendered = None
		if 'submit' in data:
			controls = data.items()
			try:
				quick_create_frm.validate(controls)
				link = Link()
				#Save the data
				link.url = data['url']

				#Set the title
				link.title = 'Untitled'
				try:
					link.title = lxml.html.parse(data['url']).find(".//title").text
				except:
					#Todo: Fix the SSL not working part....
					#http://www.webtop.com.au/blog/compiling-python-with-ssl-support-fedora-10-2009020237
					#Log error
					print ('Could not get the title of the page/url.')

				created_id = 0
				with transaction.manager as trans:
					DBSession.add(link)
					created_id = DBSession.execute(sqlalchemy.func.max(Link.id)).first()[0]

				if created_id > 0 :
					return HTTPFound(self.request.route_url('link_edit', id=created_id))
			except deform.ValidationFailure as e:
				quick_create_frm_rendered = e.render()

		if quick_create_frm_rendered is None:
			quick_create_frm_rendered = quick_create_frm.render()

		return {
			'quickCreateFrm': quick_create_frm_rendered,
			'linkLst': linksLst,
		}

	@view_config(route_name='link_create', renderer='templates/link/create.mako')
	def create(self):
		print('link:create')
		form = self.link_form

		print(self.request.params)
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
			DBSession.add(model)

			print(self.request.POST['url'])

			self.request.session.flash(u'The link has been created successfully')

			return HTTPFound(self.request.route_url('link_list'))
		return {'form': form.render()}

	@view_config(route_name='link_edit', renderer='templates/link/edit.mako')
	def edit(self):
		id = self.request.matchdict.get('id', None)


		link = self.link_service.get_link_by_id(id)
		if link == None:
			self.request.session.flash(u'No link found with the id %s'%id)
			return Response(status=302, location=self.request.route_url("link_list"))

		schema = ShortLinkEdit()

		form = deform.Form(schema, buttons=('submit',))

		data = self.request.POST

		renderedForm = None
		if 'submit' in data:
			data['id'] = link.id

			controls = data.items()
			try:
				form.validate(controls)


				#Save the data
				self.link_service.edit_link(
					data['id'],
					title=data['title'],
					description=data['description'],
					url=data['url'],
					shorty=data['shorty'],
					tags=data['tags'])

				#Refreshing the page
				return Response(status=302, location=self.request.route_url("link_edit", id=id))
			except deform.ValidationFailure as e:
				renderedForm = e.render()

		if renderedForm is None:
			#renderedForm = form.render({'id':link.id, 'title': link.title, 'description': link.description, 'shorty': link.shorty, 'tags': ','.join(map(lambda x: x.name, link.tags)), 'url':link.url})
			renderedForm = form.render({
				'id':link.id,
				'title': link.title,
				'description': link.description,
				'shorty': link.shorty,
				'tags': ','.join(map(lambda x: x.name, link.tags)),
				'url':link.url})

		#Create the models
		model = {
			'id': id,
			'link': build_link(self.request, link),
			'hits': link.hitCount(),
			'form': renderedForm
		}

		return model

	@view_config(route_name='link_delete')
	def delete(self):
		id = self.request.matchdict.get('id', None)

		self.link_service.delete_link(id)

		self.request.session.flash(u'The link has been deleted')

		return Response(status=302, location=self.request.route_url("link_list"))