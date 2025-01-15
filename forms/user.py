from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.meta import DefaultMeta
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    FileField,
    FormField,
    IntegerField,
    PasswordField,
    SelectField,
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


class UpdateUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Email is required.")])
    is_admin = BooleanField("Is admin")

    submit = SubmitField("Save")


class DeleteUserForm(FlaskForm):
    submit = SubmitField("Delete")


class UpdateUserProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone_number = StringField("Phone number", validators=[Length(max=21)])
    address = TextAreaField("Address")
    profile_picture = FileField("Profile picture")

    submit = SubmitField("Save")


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password", validators=[DataRequired(), Length(min=8)]
    )
    new_password = PasswordField(
        "New password", validators=[DataRequired(), Length(min=8)]
    )
    confirm_new_password = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("new_password")],
    )

    submit = SubmitField("Save")


class UpdateCart(FlaskForm):
    product = SelectField("Select product", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])

    submit = SubmitField("Save")
