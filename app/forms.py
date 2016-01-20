from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class AddClassForm(Form):
    classCode = StringField('Class Code', validators=[DataRequired()])
    cohort = IntegerField('Cohort', validators=[DataRequired()])
    submit = SubmitField('Submit')
