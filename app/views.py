from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, AddClassForm


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


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
                           gsClasses= [{'classCode': '7sci_1', 'cohort': '7'},
                               {'classCode': '9t&e_1', 'cohort': '9'}],
                           user= {'firstname': 'james'})

@app.route('/classes/add', methods=['GET', 'POST'])
def addClass():
    form = AddClassForm()
    if form.validate_on_submit():
        flash('Added class, classCode=%s' %
              (form.classCode.data))
        return redirect('/classes')
    return render_template('addclass.html',
                           title='Add New Class',
                           form=form)
