from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "b0180604932321fcd23fb4ed"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cartify.db"
app.config["PROFILE_UPLOAD_FOLDER"] = "cartify/static/profile_pics"
app.config["PRODUCT_UPLOAD_FOLDER"] = "cartify/static/product_images"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


from cartify import routes
