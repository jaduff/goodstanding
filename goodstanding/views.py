from pyramid.response import Response
from pyramid.view import (
        view_config,
        view_defaults,
        )

import colander

from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (HTTPFound, HTTPNotFound,)

import deform
from deform import (widget, ValidationFailure)

from .models import (
    DBSession,
    gsClassStudent,
    gsUser,
    gsStudent,
    gsClass,
    gsClassNote
    )

from .classviews import classView


@view_config(route_name='pyramid', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(gsClass)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'goodstanding'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_goodstanding_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""



@view_defaults(renderer='templates/notImplemented.pt')
class notImplementedView:
    def __init__(self, request):
        self.request=request
        self.title = request.matched_route.pattern

