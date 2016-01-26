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

from .listView import ListView


class classView:

    def __init__(self, request):
        self.request = request


    class gsClassSchema(colander.MappingSchema):

        def check_class_exists(node, value):
            if DBSession.query(gsClass).filter_by(classCode=value['classCode']).first():
                raise colander.Invalid(node, 'This class already exists')

        classCode = colander.SchemaNode(colander.String())
        cohort = colander.SchemaNode(colander.Integer())

    @view_config(route_name='addclass', renderer='templates/formView.pt')
    @view_config(route_name='modifyclass', renderer='templates/formView.pt')
    def formView(self):
        if self.request.matched_route.name == 'modifyclass':
            schema = self.gsClassSchema()
        else:
            schema = self.gsClassSchema(validator=classView.gsClassSchema.check_class_exists)
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
        list_actions = [{'action': 'edit', 'url': '/classes/edit/', 'identifier': 'classCode'}]
        listObject = ListView(classlist, props, list_actions)
        bottomlinks = [{'name': 'Add Class', 'url': self.request.route_url("addclass")}]
        return dict(datalist=listObject.get_list(), title="My Classes", bottomlinks=bottomlinks)
