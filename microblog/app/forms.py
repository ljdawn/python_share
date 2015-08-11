from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField, validators
from wtforms.validators import DataRequired
from models import User, Post

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)

    def __init__(self, *args, **kargs):
        Form.__init__(self, *args, **kargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username = self.username.data).first()
        if user is None:
            self.username.errors.append("unkonwn")
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append("invalid password")
            return False
        self.user = user
        return True

class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message="password must match")
    ])
    email = TextField("Email Address", validators.Email("requires a valid email"))
    confirm = PasswordField("Repeat PassWord")
    remember_me = BooleanField('remember_me', default=False)
