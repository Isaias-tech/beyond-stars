from wtforms.validators import DataRequired, Length, EqualTo, Optional, Email
from wtforms.meta import DefaultMeta
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    FormField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Email is required.")])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")


class UserProfileForm(FlaskForm):
    class Meta(DefaultMeta):
        csrf = False

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    profile = FormField(UserProfileForm)
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )

    submit = SubmitField("Register")


class UserProfileForm(FlaskForm):
    class Meta:
        csrf = False

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[Optional()])
    address = TextAreaField("Address", validators=[Optional()])


class UserUpdateForm(FlaskForm):
    profile = FormField(UserProfileForm)
    email = EmailField("Email", validators=[DataRequired(), Email()])
    is_admin = BooleanField("Admin Privileges")
    submit = SubmitField("Update User")


class PasswordUpdateForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm New Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Update Password")


class AccountDeleteForm(FlaskForm):
    confirm_delete = BooleanField(
        "I confirm I want to delete this account", validators=[DataRequired()]
    )
    submit = SubmitField("Delete Account")
