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

class ListView:

    def __init__(self, objectList, propArray, actionArray):
        #objectList - array of objects with properties to serialise
        #propArray - array of dicts containing the property to serialise from objectList, and the name to display in the table header. Expect key of prop and name.
        #actionArray - array of action dicts to append to the end of each row. Expect keys of action and url. Action is the word to and url is the action. If the action requires a unique identifer, the key will be identifier.

        self.listheaders = [] #simple array of header names
        self.rows = [] #dictionary of data: dataArray, action: actionArray

        for propDict in propArray:
            self.listheaders.append(propDict['name']) #add each name to the header

        for obj in objectList:
            row = {}
            row['data'] = []
            row['actions'] = []
            for propDict in propArray:
                row['data'].append(str(getattr(obj, propDict['prop']))) #add array of data
            for action in actionArray:
                if 'identifier'in  action:
                    url = action['url'] + str(getattr(obj, action['identifier']))
                else:
                    url = action['url']
                row['actions'].append({'action': action['action'], 'url': url})
            self.rows.append(row)

    def get_headers(self):
        return self.listheaders

    def get_rows(self):
        return self.rows

    def get_list(self):
        datadict = {'headers': self.listheaders, 'data': self.rows}
        return datadict


class classView:

    def __init__(self, request):
        self.request = request


    class gsClassSchema(colander.MappingSchema):
        def check_class_exists_validator(node, value):
            if DBSession.query(gsClass).filter_by(classCode=value).first():
                raise colander.Invalid(node, 'This class already exists')
        classCode = colander.SchemaNode(colander.String(),
                validator=check_class_exists_validator)
        cohort = colander.SchemaNode(colander.Integer())

    @view_config(route_name='addclass', renderer='templates/formView.pt')
    @view_config(route_name='modifyclass', renderer='templates/formView.pt')
    def formView(self):
        schema = self.gsClassSchema()
        classform = deform.Form(schema, buttons=('submit',))
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()

            try:
                appstruct = classform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}
            #need validation to check if this classcode already used by this teacher
            #maybe reload form with schema as provided, but add an error message at the top? Flash message?
            gsclass = gsClass(classCode=appstruct['classCode'], cohort=appstruct['cohort'])
            DBSession.add(gsclass)
            return HTTPFound(self.request.route_url("listclasses"))
        if self.request.matched_route.name == 'modifyclass':
            gsclass = DBSession.query(gsClass).filter_by(classCode=self.request.matchdict['classcode']).first()
            appstruct = {'classCode': gsclass.classCode, 'cohort': gsclass.cohort}
            form = classform.render(appstruct)
        else:
            form = classform.render()
        return dict(form=form)

    @view_config(route_name='listclasses', renderer='templates/listView.pt')
    def listView(self):
        classlist = DBSession.query(gsClass).all()
        props = [{'prop': 'classCode', 'name': 'Class Code'}, {'prop': 'cohort', 'name': 'Cohort'}]
        list_actions = [{'action': 'edit', 'url': '/classes/edit/', 'identifier': 'classCode'}, {'action': 'delete', 'url': '/classes/delete/'}]
        listObject = ListView(classlist, props, list_actions)
        return dict(datalist=listObject.get_list(), title="My Classes")


@view_defaults(renderer='templates/notImplemented.pt')
class notImplementedView:
    def __init__(self, request):
        self.request=request
        self.title = request.matched_route.pattern

    @view_config(route_name='liststudents')
    def listclasses(self):
        return dict(title=self.title)

    @view_config(route_name='addstudent')
    def listclasses(self):
        return dict(title=self.title)

    @view_config(route_name='modifystudent')
    def listclasses(self):
        return dict(title=self.title)
