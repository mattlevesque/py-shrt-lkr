import colander
import deform.widget
from pyramid.httpexceptions import HTTPFound

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

# http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/forms.html

class ShortLink(colander.MappingSchema):
	description = colander.SchemaNode(colander.String())
	full = colander.SchemaNode(
		colander.String(),
		widget=deform.widget.RichTextWidget(delayed_load=True),
		title='Full frontal description'
	)


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
	def hit(self):
		return Response(status=302, location="http://www.example.com/")

	@view_config(route_name='link_list', renderer='templates/link/list.mako')
	def list(self):
		return {'data': "TEST"}

	@view_config(route_name='link_create', renderer='templates/link/create.mako')
	def create(self):
		print('link:create')
		form = self.link_form.render()

		print (self.request.params)
		print('submit' in self.request.POST)

		if 'submit' in self.request.POST:
			controls = self.request.POST.items()
			try:
				print('try')
				appstruct = self.link_form.validate(controls)
			except deform.ValidationFailure as e:
				print('except')
				return {'test': '<h5>Bad entry... RETRY!!!</h5>', 'form': e.render()}
			return HTTPFound("/yes-it-validated")
		return {'test': '<h5>TEST</h5>', 'form': form}

	@view_config(route_name='link_edit', renderer='templates/link/edit.mako')
	def edit(self):
		id = self.request.matchdict.get('id', None)
		return {'data': "TEST", 'id': id}