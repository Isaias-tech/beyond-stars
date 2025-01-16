from flask_wtf import FlaskForm
from wtforms import (
    MultipleFileField,
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectMultipleField,
    SubmitField,
)
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    title = StringField(
        "Product Title",
        validators=[DataRequired(), Length(max=250)],
    )
    sub_title = StringField(
        "Product Subtitle",
        validators=[Length(max=500)],
    )
    properties = TextAreaField(
        "Product Properties (JSON format)",
        validators=[DataRequired()],
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
    )
    price = DecimalField(
        "Price (USD)",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    stocks = IntegerField(
        "Stock Quantity",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    categories = SelectMultipleField(
        "Categories",
        coerce=int,  # Assumes category IDs will be integers
        validators=[DataRequired()],
    )

    pictures = MultipleFileField(
        "Product Pictures",
        validators=[
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!"),
        ],
    )
    submit = SubmitField("Save Product")


class CategoryForm(FlaskForm):
    name = StringField(
        "Category Name",
        validators=[DataRequired(), Length(max=100)],
    )
    submit = SubmitField("Save Category")


class DeleteProductForm(FlaskForm):
    confirm_delete = SubmitField("Delete Product")


class DeleteCategoryForm(FlaskForm):
    confirm_delete = SubmitField("Delete Category")
