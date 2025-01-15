from flask_login import current_user, login_required
from flask import Blueprint, render_template


admin_blueprints = Blueprint("admin", __name__, url_prefix="/admin")


@admin_blueprints.context_processor
def inject_authenticated_user():
    if current_user.is_authenticated:
        return {"user": current_user}
    return {"user": None}


@admin_blueprints.route("/profile", methods=["GET"])
@login_required
def admin_profile_page():
    return render_template("admin/profile.html")


@admin_blueprints.route("/profile/update", methods=["GET", "PUT", "PATCH"])
@login_required
def update_admin_profile_page():
    return render_template("admin/update_profile.html")


@admin_blueprints.route("/products", methods=["GET"])
@login_required
def products_management_page():
    return render_template("admin/products/products_management.html")


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
    return render_template("admin/users/user_management.html")


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
    return render_template("admin/transactions/transaction_details.html")


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
    return render_template("admin/product_categories/category_management.html")


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
