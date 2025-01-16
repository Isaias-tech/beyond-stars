from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, logout_user


private_blueprints = Blueprint("private", __name__)


@private_blueprints.route("/profile", methods=["GET"])
@login_required
def profile_page():
    return render_template("private/profile.html")


@private_blueprints.route("/logout", methods=["GET"])
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("public.login_page"))


@private_blueprints.route("/cart", methods=["GET", "POST"])
@login_required
def cart_page():
    return render_template("private/cart.html")


@private_blueprints.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout_page():
    return render_template("private/checkout.html")


@private_blueprints.route("/payment-completed", methods=["GET"])
@login_required
def payment_completed_page():
    return render_template("private/payment_completed.html")


@private_blueprints.route("/transactions", methods=["GET"])
@login_required
def transactions_page():
    return render_template("private/transaction.html")


@private_blueprints.route("/transactions/<int:id>", methods=["GET"])
@login_required
def transaction_details_page():
    return render_template("private/transaction_detail.html")


@private_blueprints.route("/transactions/<int:id>/cancel", methods=["GET", "POST"])
@login_required
def cancel_transaction_page():
    return render_template("private/cancel_transaction.html")
