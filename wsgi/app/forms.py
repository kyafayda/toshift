from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required, Length, TextAreaField

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class PostExpense(Form):
    type = TextField('type', validators = [Required()])
    amount = TextField('amount', validators = [Required()])
    description = TextField('description')
    vendor = TextField('vendor', validators = [Required()])
    date = TextField('date')
    mode = TextField('mode', validators = [Required()])

