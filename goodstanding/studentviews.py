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


class studentView:

    def __init__(self, request):
        self.request = request


    class gsStudentSchema(colander.MappingSchema):

        def check_student_exists(node, value):
            if DBSession.query(gsStudent).filter_by(id=value['id']).first():
                raise colander.Invalid(node, 'This student already exists')

        id= colander.SchemaNode(colander.Integer())
        FirstName = colander.SchemaNode(colander.String())
        LastName = colander.SchemaNode(colander.String())
        username = colander.SchemaNode(colander.String(), missing="") 
        cohort = colander.SchemaNode(colander.Integer())
        current = colander.SchemaNode(colander.Boolean(), default=True)

    @view_config(route_name='addstudent', renderer='templates/formView.pt')
    def formView(self):
        #addstudent does not allow submission of already existing student
        schema = self.gsStudentSchema(validator=studentView.gsStudentSchema.check_student_exists)
        studentform = deform.Form(schema, buttons=('submit',))

        if 'submit' in self.request.POST:
            #Handle submitted form
            controls = self.request.POST.items()

            try:
                #validate form
                appstruct = studentform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}


            #populate gsstudent with data from validated form, ready to submit to database
            gsstudent = gsStudent(id=appstruct['id'], FirstName=appstruct['FirstName'], LastName=appstruct['LastName'], cohort=appstruct['cohort'], current=appstruct['current'])
            DBSession.add(gsstudent)

            #After successful form submission, return to list of students
            return HTTPFound(self.request.route_url("liststudents"))

        #render blank form for creation of new student
        form = studentform.render()
        return dict(form=form)

    @view_config(route_name='modifystudent', renderer='templates/formView.pt')
    def formView(self):
        rstudentid= self.request.matchdict['studentid']
        #check that student exists before continuing
        gsstudent = DBSession.query(gsStudent).filter_by(id=rstudentid).first()
        if not gsstudent:
            detail = "Student " + rstudentid + " does not exist."
            return HTTPNotFound(comment='Student does not exist', detail=detail)
        #modifystudent allows database submission of existing student
        schema = self.gsStudentSchema()
        studentform = deform.Form(schema, buttons=('submit',))

        if 'submit' in self.request.POST:
            #Handle submitted form
            controls = self.request.POST.items()

            try:
                #validate form
                appstruct = studentform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}


            #populate gsstudent with data from validated form, ready to submit to database
            gsstudent.id=appstruct['id']
            gsstudent.FirstName=appstruct['FirstName']
            gsstudent.LastName=appstruct['LastName']
            gsstudent.cohort=appstruct['cohort']
            gsstudent.current=appstruct['current']
            DBSession.add(gsstudent)

            #After successful form submission, return to list of students
            return HTTPFound(self.request.route_url("liststudents"))

        #modifystudent requires form to be prefilled with data from the database
        appstruct = {'id': gsstudent.id, 'FirstName': gsstudent.FirstName, 'LastName': gsstudent.LastName, 'cohort': gsstudent.cohort, 'current': gsstudent.current}
        form = studentform.render(appstruct)
        return dict(form=form)

    @view_config(route_name='liststudents', renderer='templates/listView.pt')
    def listView(self):
        studentlist = DBSession.query(gsStudent).all()
        props = [{'prop': 'FirstName', 'name': 'First Name'}, {'prop': 'LastName', 'name': 'Last Name'},  {'prop': 'cohort', 'name': 'Cohort'}, {'prop': 'current', 'name': 'Cohort'}]
        list_actions = [{'action': 'edit', 'url': '/students/modify', 'identifier': 'id'}]
        listObject = ListView(studentlist, props, list_actions)
        bottomlinks = [{'name': 'Add Student', 'url': self.request.route_url("addstudent")}]
        return dict(datalist=listObject.get_list(), title="Students", bottomlinks=bottomlinks)
