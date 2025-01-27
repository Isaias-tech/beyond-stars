from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, flash, json, redirect, render_template, request, url_for
from decorators.auth_decorators import redirect_if_authenticated
from forms.user import LoginForm, RegisterForm, LogoutForm
from flask_login import login_user, current_user
from app import user as userModels, db, product as productModels

public_blueprints = Blueprint("public", __name__)


@public_blueprints.route("/", methods=["GET"])
@redirect_if_authenticated
def landing_page():
    # Fetch the first 8 products
    products = (
        productModels.Product.query.order_by(productModels.Product.id.asc())
        .limit(8)
        .all()
    )

    return render_template("landing.html", products=products)


@public_blueprints.route("/login", methods=["GET", "POST"])
@redirect_if_authenticated
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.data.get("email").strip().lower()
        password = form.data.get("password")

        user = userModels.User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("public.products_page"))
        else:
            flash("Invalid email or password. Please try again.", "error")

    return render_template("auth/login_form.html", form=form)


@public_blueprints.route("/register", methods=["GET", "POST"])
@redirect_if_authenticated
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        if userModels.User.query.filter_by(
            email=form.email.data.strip().lower()
        ).first():
            flash("Email already exists!", "error")
        else:
            try:
                hashed_password = generate_password_hash(form.password.data)
                new_user = userModels.User(
                    email=form.email.data,
                    password=hashed_password,
                )
                user_profile = userModels.UserProfile(
                    first_name=form.profile.first_name.data,
                    last_name=form.profile.last_name.data,
                    user=new_user,
                )
                db.session.add(new_user)
                db.session.add(user_profile)
                db.session.commit()
                flash("User registered successfully!", "success")
                return redirect(url_for("public.login_page"))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {str(e)}", "error")

    return render_template("auth/register_form.html", form=form)


@public_blueprints.route("/products", methods=["GET"])
def products_page():
    # Default context for user authentication
    context = {"user": None, "products": [], "categories": []}

    if current_user.is_authenticated:
        profile = userModels.UserProfile.query.filter_by(
            user_id=current_user.id
        ).first()
        context["user"] = current_user
        context["profile"] = profile
        context["form"] = LogoutForm()

    # Search and filter logic
    search_query = request.args.get("search", "").strip()
    category_id = request.args.get("category", "").strip()

    # Query products
    products_query = productModels.Product.query

    # Apply search filter
    if search_query:
        products_query = products_query.filter(
            productModels.Product.title.ilike(f"%{search_query}%")
            | productModels.Product.description.ilike(f"%{search_query}%")
        )

    # Apply category filter
    if category_id:
        products_query = products_query.join(productModels.Product.categories).filter(
            productModels.ProductCategory.id == category_id
        )

    # Fetch filtered products
    products = products_query.all()

    # Fetch all categories for the filter dropdown
    categories = productModels.ProductCategory.query.all()

    # Add products and categories to the context
    context["products"] = products
    context["categories"] = categories

    return render_template("public/products.html", **context)


@public_blueprints.route("/products/<int:id>", methods=["GET"])
def product_details_page(id: int):
    # Default context for user authentication
    context = {"user": None, "product": None}

    if current_user.is_authenticated:
        profile = userModels.UserProfile.query.filter_by(
            user_id=current_user.id
        ).first()
        context["user"] = current_user
        context["profile"] = profile
        context["form"] = LogoutForm()

    # Fetch the product by ID
    product = productModels.Product.query.get_or_404(id)
    context["product"] = product

    product_properties = json.loads(product.properties)

    return render_template(
        "public/product_details.html", **context, product_properties=product_properties
    )
