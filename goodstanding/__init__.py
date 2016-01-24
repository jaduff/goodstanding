from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    gsClass,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('pyramid', '/pyramid')
    config.add_route('listclasses', '/classes')
    config.add_route('addclass', '/classes/add')
    config.add_route('modifyclass', '/classes/{action}/{class}')
    config.add_route('Home', '/')
    config.add_route('liststudents', '/students')
    config.add_route('addstudent', '/students/add')
    config.add_route('modifystudent', '/students/{action}/{studentid}')
    config.scan()
    return config.make_wsgi_app()
