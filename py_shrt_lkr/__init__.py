from pyramid.config import Configurator
from pyramid.events import BeforeRender
from sqlalchemy import engine_from_config

import webhelpers2.html.tags as tags
import pyramid.url as url
from pyramid.session import SignedCookieSessionFactory


from .models import (
	DBSession,
	Base,
)


def add_referer_globals(event):
	event['tags'] = tags
	event['url'] = url

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine

	shrt_lkr_session_factory = SignedCookieSessionFactory('SoF4K1n6S3cr3T')

	config = Configurator(settings=settings)
	config.set_session_factory(shrt_lkr_session_factory)
	config.include('pyramid_mako')
	config.add_subscriber(add_referer_globals, BeforeRender)

	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('home', '/')

	config.add_route('link_list', '/admin/link/')
	config.add_route('link_create', '/admin/link/new')
	config.add_route('link_edit', '/admin/link/{id}')
	config.add_route('link_delete', '/admin/link/delete/{id}')

	config.add_route('link_hit', '/{hashids}')


	config.add_static_view('deform_static', 'deform:static/')
	#config.add_static_view('static', 'deform:static')

	config.scan()
	return config.make_wsgi_app()
