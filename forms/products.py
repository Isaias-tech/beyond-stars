from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)


class ProductForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=250)])
    sub_title = StringField("Sub title", validators=[DataRequired(), Length(max=500)])
    properties = SelectMultipleField("Properties", validators=[DataRequired()])
    property_value = StringField("Property value", validators=[DataRequired()])
    description = TextAreaField("Description")
    price = FloatField("Price", validators=[DataRequired()])
    stocks = IntegerField("Stoks", validators=[DataRequired()])

    submit = SubmitField("Save")


class AddProductPictureForm(FlaskForm):
    product = SelectField("Product", validators=[DataRequired()])
    url = TextAreaField("URL", validators=[DataRequired()])

    submit = SubmitField("Save")
