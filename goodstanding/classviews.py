from pyramid.response import Response
from pyramid.view import (
        view_config,
        view_defaults,
        )

import colander

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import exc

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

class Student(colander.MappingSchema):
    studentid = colander.SchemaNode(colander.Integer())
    FirstName = colander.SchemaNode(colander.String())
    LastName = colander.SchemaNode(colander.String())

class Students(colander.SequenceSchema):
    Students = Student()

class gsClassSchema(colander.MappingSchema):
    #validator to check if class already exists
    def check_class_exists(node, value):
        try:
            gsclass = DBSession.query(gsClass).filter_by(classCode=value['classCode']).one()
        except exc.NoResultFound:
            pass
        except exc.MultipleResultsFound:
            raise colander.Invalid(node, 'This class already exists')

    #class details
    classCode = colander.SchemaNode(colander.String(), title="Class Code")
    cohort = colander.SchemaNode(colander.Integer(), title="Cohort")
    students = Students()

class classView():

    def __init__(self, request):
        self.request = request


    @view_config(route_name='addclass', renderer='templates/formView.pt')
    def addformView(self):
        #addclass does not allow submission of already existing class
        schema = gsClassSchema(validator=gsClassSchema.check_class_exists)
        classform = deform.Form(schema, buttons=('submit',))

        if 'submit' in self.request.POST:
            #Handle submitted form
            controls = self.request.POST.items()

            try:
                #validate form
                appstruct = classform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}


            #populate gsclass with data from validated form, ready to submit to database
            gsclass = gsClass(classCode=appstruct['classCode'], cohort=appstruct['cohort'])
            DBSession.add(gsclass)

            #After successful form submission, return to list of classes
            return HTTPFound(self.request.route_url("listclasses"))

        #render blank form for creation of new class
        form = classform.render()
        return dict(form=form)

    @view_config(route_name='modifyclass', renderer='templates/formView.pt')
    def modifyformView(self):
        rclasscode = self.request.matchdict['classcode']
        #check that class exists before continuing
        try:
            gsclass = DBSession.query(gsClass).filter_by(classCode=rclasscode).one()
        except exc.NoResultFound:
            detail = "Class " + rclasscode + " does not exist."
            return HTTPNotFound(comment='Class does not exist', detail=detail)
        #modifyclass allows database submission of existing class
        schema = gsClassSchema()
        if 'Delete' in self.request.POST:
            confirm_delete = deform.Button(name='confirm_delete', css_class='delete button', title="Yes, really delete " + self.request.params['classCode'])
            classform = deform.Form(schema, buttons=(confirm_delete,))
        elif 'confirm_delete' in self.request.POST:
            DBSession.delete(gsclass)
            return HTTPFound(self.request.route_url("listclasses"))
        else:
            classform = deform.Form(schema, buttons=('Delete', 'Submit'))

        if 'submit' in self.request.POST:
            #Handle submitted form
            controls = self.request.POST.items()

            try:
                #validate form
                appstruct = classform.validate(controls)
            except ValidationFailure as e:
                return {'form':e.render()}


            #populate gsclass with data from validated form, ready to submit to database
            gsclass.classCode=appstruct['classCode']
            gsclass.cohort=appstruct['cohort']
            DBSession.add(gsclass)

            #After successful form submission, return to list of classes
            return HTTPFound(self.request.route_url("listclasses"))

        #modifyclass requires form to be prefilled with data from the database
        allstudents = DBSession.query(gsStudent).filter_by(cohort=gsclass.cohort).order_by(gsStudent.LastName).all()
        studentsstruct = []
        for student in allstudents:
            studentsstruct.append({'studentid': student.id, 'FirstName': student.FirstName, 'LastName': student.LastName})
        appstruct = {'classCode': gsclass.classCode, 'cohort': gsclass.cohort, 'students': studentsstruct}
        form = classform.render(appstruct)
        return dict(form=form)

    @view_config(route_name='listclasses', renderer='templates/classlistView.pt')
    def listclassesView(self):
        gsclasses = DBSession.query(gsClass).all()
        bottomlinks = [{'name': 'Add Class', 'url': self.request.route_url("addclass")}]
        return dict(gsclasses=gsclasses, title="My Classes", bottomlinks=bottomlinks, req=self.request)

    @view_config(route_name='viewclass', renderer='templates/classstudentsView.pt')
    def classstudentsView(self):
        rclasscode = self.request.matchdict['classcode']
        try:
            gsclass = DBSession.query(gsClass).filter_by(classCode=rclasscode).one()
        except exc.NoResultFound:
            detail = "Class " + rclasscode + " does not exist."
            return HTTPNotFound(comment='Class does not exist', detail=detail)
        bottomlinks = [{'name': 'Edit Class', 'url': self.request.route_url("modifyclass", classcode=gsclass.classCode)}]
        return dict(gsclass=gsclass, bottomlinks=bottomlinks, req=self.request)
