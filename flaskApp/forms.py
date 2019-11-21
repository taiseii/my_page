from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import  DataRequired, Length, Email, EqualTo, ValidationError
from flaskApp.models import User

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('LOG IN')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    link = TextAreaField('Link', validators=[DataRequired()])
    submit = SubmitField('Add')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError('Not in the system.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')