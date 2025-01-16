from flask_login import current_user, login_required
from flask import Blueprint, flash, redirect, render_template, url_for
from app import (
    user as userModels,
    product as productModels,
    transaction as transactionModels,
)
from decorators.auth_decorators import is_admin_validator
from forms.products import (
    CategoryForm,
    DeleteCategoryForm,
    DeleteProductForm,
    ProductForm,
)
from forms.user import (
    AccountDeleteForm,
    DeleteUserForm,
    PasswordUpdateForm,
    RegisterForm,
    UserForm,
    UserUpdateForm,
)
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import current_app, request
from werkzeug.utils import secure_filename

admin_blueprints = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprints.context_processor
def inject_authenticated_user():
    context = {"user": None}
    if current_user.is_authenticated:
        context["user"] = current_user
        return context
    return context


@admin_blueprints.route("/profile", methods=["GET"])
@login_required
@is_admin_validator
def admin_profile_page():
    return render_template("admin/profile.html")


@admin_blueprints.route("/profile/update", methods=["GET", "POST"])
@login_required
@is_admin_validator
def update_admin_profile_page():
    form = UserUpdateForm(obj=current_user)

    if current_user.user_profile:
        form.profile.form.first_name.data = current_user.user_profile.first_name
        form.profile.form.last_name.data = current_user.user_profile.last_name
        form.profile.form.phone_number.data = current_user.user_profile.phone_number
        form.profile.form.address.data = current_user.user_profile.address

    if form.validate_on_submit():
        # Update User
        current_user.email = form.email.data
        current_user.is_admin = form.is_admin.data

        # Update UserProfile
        current_user.user_profile.first_name = form.profile.first_name.data
        current_user.user_profile.last_name = form.profile.last_name.data
        current_user.user_profile.phone_number = form.profile.phone_number.data
        current_user.user_profile.address = form.profile.address.data

        db.session.commit()
        flash("Your profile has been updated successfully!", "success")
        return redirect(url_for("admin.admin_profile_page"))

    return render_template("admin/update_profile.html", form=form)


@admin_blueprints.route("/profile/update-password/", methods=["GET", "POST"])
@login_required
@is_admin_validator
def change_admin_password():
    form = PasswordUpdateForm()

    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect.", "danger")
        elif form.new_password.data != form.confirm_password.data:
            flash("New password and confirmation do not match.", "danger")
        else:
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash("Your password has been changed successfully!", "success")
            return redirect(url_for("admin.admin_profile_page"))

    return render_template("admin/update_password.html", form=form)


@admin_blueprints.route("/profile/delete/", methods=["GET", "POST"])
@login_required
@is_admin_validator
def delete_admin_account():
    form = AccountDeleteForm()

    if form.validate_on_submit():
        if form.confirm_delete.data:
            # Delete the current user's account
            db.session.delete(current_user)
            db.session.commit()
            flash("Your account has been deleted successfully.", "success")
            return redirect(url_for("public.landing_page"))

        flash("Account deletion not confirmed.", "warning")

    return render_template("admin/delete_account.html", form=form)


@admin_blueprints.route("/users", methods=["GET"])
@login_required
@is_admin_validator
def users_management_page():
    context = {"users": userModels.User.query.all()}
    return render_template("admin/users/user_management.html", **context)


@admin_blueprints.route("/users/<int:id>", methods=["GET"])
@login_required
@is_admin_validator
def user_details_page(id: int):
    user = userModels.User.query.get_or_404(id)
    return render_template("admin/users/user_details.html", user=user)


@admin_blueprints.route("/users/create", methods=["GET", "POST"])
@login_required
@is_admin_validator
def create_user_page():
    form = RegisterForm()

    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Create a new user
        new_user = userModels.User(
            email=form.email.data,
            is_admin=False,  # Default to non-admin, can be adjusted based on form logic
            password=hashed_password,
        )

        # Create associated profile
        new_user_profile = userModels.UserProfile(
            first_name=form.profile.first_name.data,
            last_name=form.profile.last_name.data,
            user=new_user,
        )

        db.session.add(new_user)
        db.session.add(new_user_profile)
        db.session.commit()
        flash("User created successfully!", "success")
        return redirect(url_for("admin.user_details_page", id=new_user.id))

    return render_template("admin/users/create_user.html", form=form)


@admin_blueprints.route("/users/<int:id>/update", methods=["GET", "POST"])
@login_required
@is_admin_validator
def update_user_page(id: int):
    user = userModels.User.query.get_or_404(id)
    form = UserForm(
        obj=user,
        profile={
            "first_name": user.user_profile.first_name if user.user_profile else "",
            "last_name": user.user_profile.last_name if user.user_profile else "",
            "phone_number": user.user_profile.phone_number if user.user_profile else "",
            "address": user.user_profile.address if user.user_profile else "",
        },
    )

    if form.validate_on_submit():
        print("Form is valid and submitted.")  # Debugging: Check if validation passes

        # Update user fields
        user.email = form.email.data
        user.is_admin = form.is_admin.data

        # Update profile fields
        if user.user_profile:
            user.user_profile.first_name = form.profile.first_name.data
            user.user_profile.last_name = form.profile.last_name.data
            user.user_profile.phone_number = form.profile.phone_number.data
            user.user_profile.address = form.profile.address.data

        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.user_details_page", id=user.id))

    # Debugging: Show form errors if any
    if form.errors:
        print("Form errors:", form.errors)

    return render_template("admin/users/update_user.html", form=form, user=user)


@admin_blueprints.route("/users/<int:id>/delete", methods=["GET", "POST"])
@login_required
@is_admin_validator
def delete_user_page(id: int):
    user = userModels.User.query.get_or_404(id)
    form = DeleteUserForm()

    if form.validate_on_submit():
        if form.confirm_delete.data:
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully!", "success")
            return redirect(url_for("admin.users_management_page"))

        flash("Account deletion not confirmed.", "warning")

    return render_template("admin/users/delete_user.html", form=form, user=user)


@admin_blueprints.route("/transactions", methods=["GET"])
@login_required
@is_admin_validator
def transactions_page():
    context = {"transactions": transactionModels.Transaction.query.all()}
    return render_template("admin/transactions/transaction_details.html", **context)


@admin_blueprints.route("/transactions/<int:id>", methods=["GET"])
@login_required
@is_admin_validator
def transactions_details_page(id: int):
    return render_template("admin/transactions/cancel_transaction.html")


@admin_blueprints.route(
    "/transactions/<int:id>/cancel", methods=["GET", "PUT", "PATCH"]
)
@login_required
@is_admin_validator
def cancel_transactions_page(id: int):
    return render_template("admin/transactions/transaction_details.html")


@admin_blueprints.route("/products", methods=["GET"])
@login_required
@is_admin_validator
def products_management_page():
    context = {"products": productModels.Product.query.all()}
    return render_template("admin/products/products_management.html", **context)


@admin_blueprints.route("/products/<int:id>", methods=["GET", "POST"])
@login_required
@is_admin_validator
def product_details_page(id: int):
    product = productModels.Product.query.get_or_404(id)

    if request.method == "POST":
        if "remove_pictures" in request.form:
            picture_ids = request.form.getlist("remove_pictures")
            productModels.ProductPicture.query.filter(
                productModels.ProductPicture.id.in_(picture_ids)
            ).delete(synchronize_session=False)
            db.session.commit()
            flash("Selected pictures were successfully removed.", "success")
            return redirect(url_for("admin.product_details_page", id=id))

    return render_template(
        "admin/products/product_details.html",
        product=product,
    )


@admin_blueprints.route("/products/create", methods=["GET", "POST"])
@login_required
@is_admin_validator
def create_product_page():
    form = ProductForm()
    form.categories.choices = [
        (category.id, category.name)
        for category in productModels.ProductCategory.query.all()
    ]

    if form.validate_on_submit():
        new_product = productModels.Product(
            title=form.title.data,
            sub_title=form.sub_title.data,
            properties=form.properties.data,
            description=form.description.data,
            price=form.price.data,
            stocks=form.stocks.data,
        )
        # Assign categories
        new_product.categories = productModels.ProductCategory.query.filter(
            productModels.ProductCategory.id.in_(form.categories.data)
        ).all()

        db.session.add(new_product)
        db.session.commit()
        flash("Product created successfully!", "success")
        return redirect(url_for("admin.product_details_page", id=new_product.id))

    return render_template("admin/products/create_product.html", form=form)


@admin_blueprints.route("/products/<int:id>/update", methods=["GET", "POST"])
@login_required
@is_admin_validator
def update_product_page(id: int):
    product = productModels.Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.categories.choices = [
        (category.id, category.name)
        for category in productModels.ProductCategory.query.all()
    ]

    # Pre-fill selected categories
    form.categories.data = [category.id for category in product.categories]

    if form.validate_on_submit():
        # Update product fields
        product.title = form.title.data
        product.sub_title = form.sub_title.data
        product.properties = form.properties.data
        product.description = form.description.data
        product.price = form.price.data
        product.stocks = form.stocks.data

        # Update categories
        product.categories = productModels.ProductCategory.query.filter(
            productModels.ProductCategory.id.in_(form.categories.data)
        ).all()

        # Handle new pictures
        if form.pictures.data:
            upload_folder = os.path.join(
                current_app.root_path, current_app.config["UPLOAD_FOLDER"]
            )
            os.makedirs(upload_folder, exist_ok=True)

            for picture in form.pictures.data:
                # Secure the filename
                filename = secure_filename(picture.filename)
                filepath = os.path.join(upload_folder, filename)
                picture.save(filepath)

                # Add picture to the database
                new_picture = productModels.ProductPicture(
                    url=f"/{current_app.config['UPLOAD_FOLDER']}/{filename}",
                    product_id=product.id,
                )
                db.session.add(new_picture)

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("admin.product_details_page", id=product.id))

    return render_template(
        "admin/products/update_product.html", form=form, product=product
    )


@admin_blueprints.route("/products/<int:id>/delete", methods=["GET", "POST"])
@login_required
@is_admin_validator
def delete_product_page(id: int):
    product = productModels.Product.query.get_or_404(id)
    form = DeleteProductForm()

    if form.validate_on_submit():
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully!", "success")
        return redirect(url_for("admin.category_management_page"))

    return render_template(
        "admin/products/delete_product.html", form=form, product=product
    )


@admin_blueprints.route("/product-categories", methods=["GET"])
@login_required
@is_admin_validator
def category_management_page():
    context = {"categories": productModels.ProductCategory.query.all()}
    return render_template(
        "admin/product_categories/category_management.html", **context
    )


@admin_blueprints.route("/product-categories/create", methods=["GET", "POST"])
@login_required
@is_admin_validator
def create_category_page():
    form = CategoryForm()

    if form.validate_on_submit():
        new_category = productModels.ProductCategory(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash("Category created successfully!", "success")
        return redirect(url_for("admin.category_management_page"))

    return render_template("admin/product_categories/create_category.html", form=form)


@admin_blueprints.route("/product-categories/<int:id>/update", methods=["GET", "POST"])
@login_required
@is_admin_validator
def update_category_page(id: int):
    category = productModels.ProductCategory.query.get_or_404(id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("Category updated successfully!", "success")
        return redirect(url_for("admin.category_management_page"))

    return render_template(
        "admin/product_categories/update_category.html", form=form, category=category
    )


@admin_blueprints.route("/product-categories/<int:id>/delete", methods=["GET", "POST"])
@login_required
@is_admin_validator
def delete_category_page(id: int):
    category = productModels.ProductCategory.query.get_or_404(id)
    form = DeleteCategoryForm()

    if form.validate_on_submit():
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully!", "success")
        return redirect(url_for("admin.category_management_page"))

    return render_template(
        "admin/product_categories/delete_category.html", form=form, category=category
    )
