import colander
import deform.widget

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
	DBSession,
	MyModel,
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


class ShortLink(colander.MappingSchema):
	description = colander.SchemaNode(colander.String())


class LinkViews(object):
	def __init__(self, request):
		self.request = request

	@property
	def link_form(self):
		schema = ShortLink()
		return deform.Form(schema, buttons=('submit',))

	@property
	def reqts(self):
		return self.link_form.get_widget_resources()

	@view_config(route_name='link_hit')
	def link_hit(self):
		return Response(status=302, location="http://www.example.com/")

	@view_config(route_name='link_list', renderer='templates/link/list.mako')
	def link_list(self):
		return {'data': "TEST"}

	@view_config(route_name='link_create', renderer='templates/link/create.mako')
	def link_create(self):
		form = self.link_form.render()
		return {'test': '<h5>TEST</h5>', 'form': form}

	@view_config(route_name='link_edit', renderer='templates/link/edit.mako')
	def link_edit(self):
		id = self.request.matchdict.get('id', None)
		return {'data': "TEST", 'id': id}