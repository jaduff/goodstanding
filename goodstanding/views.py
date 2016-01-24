from pyramid.response import Response
from pyramid.view import (
        view_config,
        view_defaults,
        )

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

from .schemas import gsClassSchema


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

class classView:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='addclass', renderer='templates/formView.pt')
    def formView(self):
        schema = gsClassSchema()
        classform = deform.Form(schema, buttons=('submit',))
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()

            try:
                appstruct = classform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}
            #Do something with data
            gsclass = gsClass(classCode=appstruct['classCode'], cohort=appstruct['cohort'])
            DBSession.add(gsclass)
            return HTTPFound(self.request.route_url("Home"))
        form = classform.render()
        return dict(form=form)

    @view_config(route_name='listclasses', renderer='templates/listView.pt')
    def listView(self):
        _classlist = DBSession.query(gsClass).all()
        classlist = []
        headers = ['classCode', 'cohort']
        for gsclass in _classlist:
            classarray = []
            for prop in headers:
                classarray.append(str(getattr(gsclass, prop)))
            classlist.append(classarray)
        return dict(list=classlist, headers = headers, title="List")

@view_defaults(renderer='templates/notImplemented.pt')
class notImplementedView:
    def __init__(self, request):
        self.request=request
        self.title = request.matched_route.pattern

    @view_config(route_name='modifyclass')
    def listclasses(self):
        return dict(title=self.title)

    @view_config(route_name='liststudents')
    def listclasses(self):
        return dict(title=self.title)

    @view_config(route_name='addstudent')
    def listclasses(self):
        return dict(title=self.title)

    @view_config(route_name='modifystudent')
    def listclasses(self):
        return dict(title=self.title)
