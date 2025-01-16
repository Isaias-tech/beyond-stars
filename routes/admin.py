from flask_login import current_user, login_required
from flask import Blueprint, flash, redirect, render_template, url_for
from app import (
    user as userModels,
    product as productModels,
    transaction as transactionModels,
)
from forms.user import AccountDeleteForm, PasswordUpdateForm, UserUpdateForm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


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
def admin_profile_page():
    return render_template("admin/profile.html")


@admin_blueprints.route("/profile/update", methods=["GET", "POST"])
@login_required
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


@admin_blueprints.route("/products", methods=["GET"])
@login_required
def products_management_page():
    context = {"products": productModels.Product.query.all()}
    return render_template("admin/products/products_management.html", **context)


@admin_blueprints.route("/products/<int:id>", methods=["GET"])
@login_required
def product_details_page(id: int):
    return render_template("admin/products/product_details.html")


@admin_blueprints.route("/products/create", methods=["GET", "POST"])
@login_required
def create_product_page():
    return render_template("admin/products/create_product.html")


@admin_blueprints.route("/products/<int:id>/update", methods=["GET", "PUT", "PATCH"])
@login_required
def update_product_page(id: int):
    return render_template("admin/products/update_product.html")


@admin_blueprints.route("/products/<int:id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_product_page(id: int):
    return render_template("admin/products/delete_product.html")


@admin_blueprints.route("/users", methods=["GET"])
@login_required
def users_management_page():
    context = {"users": userModels.User.query.all()}
    return render_template("admin/users/user_management.html", **context)


@admin_blueprints.route("/users/<int:id>", methods=["GET"])
@login_required
def user_details_page(id: int):
    return render_template("admin/users/user_details.html")


@admin_blueprints.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user_page():
    return render_template("admin/users/create_user.html")


@admin_blueprints.route("/users/<int:id>/update", methods=["GET", "PUT", "PATCH"])
@login_required
def update_user_page(id: int):
    return render_template("admin/users/update_user.html")


@admin_blueprints.route("/users/<int:id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_user_page(id: int):
    return render_template("admin/users/delete_user.html")


@admin_blueprints.route("/transactions", methods=["GET"])
@login_required
def transactions_page():
    context = {"transactions": transactionModels.Transaction.query.all()}
    return render_template("admin/transactions/transaction_details.html", **context)


@admin_blueprints.route("/transactions/<int:id>", methods=["GET"])
@login_required
def transactions_details_page(id: int):
    return render_template("admin/transactions/cancel_transaction.html")


@admin_blueprints.route(
    "/transactions/<int:id>/cancel", methods=["GET", "PUT", "PATCH"]
)
@login_required
def cancel_transactions_page(id: int):
    return render_template("admin/transactions/transaction_details.html")


@admin_blueprints.route("/product-categories", methods=["GET"])
@login_required
def category_management_page():
    context = {"categories": productModels.ProductCategory.query.all()}
    return render_template(
        "admin/product_categories/category_management.html", **context
    )


@admin_blueprints.route("/product-categories/create", methods=["GET", "POST"])
@login_required
def create_category_page():
    return render_template("admin/product_categories/create_category.html")


@admin_blueprints.route(
    "/product-categories/<int:id>/update", methods=["GET", "PUT", "PATCH"]
)
@login_required
def update_category_page(id: int):
    return render_template("admin/product_categories/update_category.html")


@admin_blueprints.route(
    "/product-categories/<int:id>/delete", methods=["GET", "DELETE"]
)
@login_required
def delete_category_page(id: int):
    return render_template("admin/product_categories/delete_category.html")
