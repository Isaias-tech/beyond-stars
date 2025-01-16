from extensions import db, migrate, login_manager
from routes.router import router
from dotenv import load_dotenv
from flask import Flask, send_from_directory
import os

# Models import for migration recognition
from models import user, product, transaction  # noqa: F401

app = Flask(__name__)
app.name = "Beyond Stars"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_file):
    load_dotenv(env_file)

SECRET_KEY = os.getenv("SECRET_KEY", "In$e(ur3-$3(r37-k3y")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
DEBUG = os.getenv("DEBUG", "False") == "True"

app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads", "products")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit
app.config["SECRET_KEY"] = SECRET_KEY

db.init_app(app=app)
migrate.init_app(app=app, db=db)
login_manager.init_app(app=app)
login_manager.login_view = "public.login_page"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    return user.User.query.get(int(user_id))


router(app)


@app.context_processor
def inject_app_name():
    return {"app_name": app.name}


@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=DEBUG)
