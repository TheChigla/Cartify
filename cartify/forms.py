from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    EmailField,
    PasswordField,
    FileField,
    IntegerField,
    TextAreaField,
    SelectField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from cartify.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email already exists")

    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=2, max=30)],
        render_kw={"placeholder": "First Name*", "autocomplete": "off"},
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=2)],
        render_kw={"placeholder": "Last Name*", "autocomplete": "off"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email*", "autocomplete": "off"},
    )
    profile_pic = FileField("Profile Picture")
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Password*", "autocomplete": "off"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match"),
        ],
        render_kw={"placeholder": "Confirm Password*", "autocomplete": "off"},
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Email*", "autocomplete": "off"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password*", "autocomplete": "off"},
    )
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    product_name = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Name*", "autocomplete": "off"},
    )
    product_price = IntegerField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Price*", "autocomplete": "off"},
    )
    product_quantity = IntegerField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Quantity*", "autocomplete": "off"},
    )
    product_category = SelectField(
        "Product Category",
        choices=[
            ("Vegetables", "Vegetables"),
            ("Fruits", "Fruits"),
            ("Grains", "Grains"),
            ("Snacks", "Snacks"),
            ("Meat", "Meat"),
            ("Bakery", "Bakery"),
            ("Frozen Foods", "Frozen Foods"),
            ("Cans", "Cans"),
            ("Alcohol", "Alcohol"),
            ("Sodas", "Sodas"),
        ],
        validators=[DataRequired()],
    )
    images = MultipleFileField("Product Images", validators=[DataRequired()])
    product_description = TextAreaField(
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Product Description*",
            "autocomplete": "off",
            "rows": 5,
            "cols": 30,
        },
    )
    submit = SubmitField("Add Product")


class ProductQuantityForm(FlaskForm):
    product_quantity = IntegerField(
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Product Quantity*",
            "autocomplete": "off",
            "min": 1,
        },
    )


class UpdateProductName(FlaskForm):
    product_name = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Name*", "autocomplete": "off"},
    )
    submit = SubmitField("Submit")


class UpdateProductPrice(FlaskForm):
    product_price = IntegerField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Price*", "autocomplete": "off"},
    )
    submit = SubmitField("Submit")


class UpdateProductQuantity(FlaskForm):
    product_quantity = IntegerField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Product Quantity*", "autocomplete": "off"},
    )
    submit = SubmitField("Submit")


class UpdateProductCategory(FlaskForm):
    product_category = SelectField(
        "Product Category",
        choices=[
            ("Vegetables", "Vegetables"),
            ("Fruits", "Fruits"),
            ("Grains", "Grains"),
            ("Snacks", "Snacks"),
            ("Meat", "Meat"),
            ("Bakery", "Bakery"),
            ("Frozen Foods", "Frozen Foods"),
            ("Cans", "Cans"),
            ("Alcohol", "Alcohol"),
            ("Sodas", "Sodas"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


class UpdateProductDescription(FlaskForm):
    product_description = TextAreaField(
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Product Description*",
            "autocomplete": "off",
            "rows": 5,
            "cols": 30,
        },
    )
    submit = SubmitField("Submit")
