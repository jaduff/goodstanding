from flask import render_template, flash, redirect
from app import app, db
from .forms import LoginForm, ClassForm, AddClassForm, EditClassForm, DeleteClassForm
from .models import gsClass


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Good Standing',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/classes', methods=['GET', 'POST'])
def classes():
    return render_template('classes.html',
                           title='Class List',
                           gsClasses= gsClass.query.order_by(gsClass.cohort),
                           user= {'firstname': 'james'})

@app.route('/classes/add', methods=['GET', 'POST'])
def addClass():
    form = AddClassForm()
    if form.validate_on_submit():
        if gsClass.query.filter_by(classCode=form.classCode.data).first() == None:
            gsclass = gsClass(classCode=form.classCode.data, cohort=form.cohort.data)
            db.session.add(gsclass)
            db.session.commit()
            flash('Added class, classCode=%s' %
                  (form.classCode.data))
            return redirect('/classes')
        else:
            flash('Sorry, the class %s already exists.' % (form.classCode.data))
    return render_template('modifyclass.html',
                           title='Add New Class',
                           form=form)

@app.route('/classes/modify/<classcode>', methods=['GET', 'POST'])
def modifyClass(classcode):
    gsclass = gsClass.query.filter_by(classCode=classcode).first()
    if gsclass == None:
        flash('Sorry, class ' + classcode + ' doesn\'t exist')
        return redirect('/classes')
    form = EditClassForm(obj=gsclass)
    if form.validate_on_submit():
        if form.delete.data == True:
            return redirect('/classes/delete/%s' % (form.classCode.data))
        gsclass.classCode = form.classCode.data
        gsclass.cohort = form.cohort.data
        db.session.add(gsclass)
        db.session.commit()
        flash('Modified class, classCode=%s' %
              (form.classCode.data))
        return redirect('/classes')
    form.populate_obj(gsclass)
    return render_template('modifyclass.html',
                           title='Edit Class',
                           form=form)

@app.route('/classes/delete/<classcode>', methods=['GET', 'POST'])
def deleteClass(classcode):
    gsclass = gsClass.query.filter_by(classCode=classcode).first()
    form = DeleteClassForm(obj=gsclass)
    if form.validate_on_submit():
        db.session.delete(gsclass)
        db.session.commit()
        flash('Class %s has been deleted' % (form.classCode.data))
        return redirect('/classes')
    flash('Are you sure you want to delete class %s' % (form.classCode.data))
    return render_template('modifyclass.html',
                           title='Delete Class',
                           form=form)
