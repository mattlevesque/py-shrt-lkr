import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
	get_appsettings,
	setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
	MyModel,
)

from ..core.models import (
	Base,
	DBSession,
	Link,
	LinkHit,
	Tag,
)


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri> [var=value]\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main(argv=sys.argv):
	if len(argv) < 2:
		usage(argv)
	config_uri = argv[1]
	options = parse_vars(argv[2:])
	setup_logging(config_uri)
	settings = get_appsettings(config_uri, options=options)
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)

	#Delete old data
	Base.metadata.drop_all(engine)

	Base.metadata.create_all(engine)
	with transaction.manager:
		link = Link()
		link.title = "Test 123"
		link.description = "First link"
		link.url = "https://www.google.ca/search?q=python+pyramid"
		# model = MyModel(name='one', value=1)
		link.tags = [Tag(name="Programming"), Tag(name="Python")]
		DBSession.add(link)
