from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Для label for=""
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Goal me!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # .data  - получение данных поля
        if user is not None:
            raise ValidationError('Please use a different username.')



