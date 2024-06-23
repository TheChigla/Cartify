from cartify import bcrypt, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile_pic = db.Column(db.String(100), nullable=False, default="")
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="user")
    budget = db.Column(db.Integer, nullable=False, default=1000)
    owned_products = db.relationship(
        "Product", lazy=True, foreign_keys="Product.owned_user"
    )
    bought_products = db.relationship(
        "Product", lazy=True, foreign_keys="Product.bought_user"
    )

    def __repr__(self):
        return self.email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def password(self):
        return self.password

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    password = property(password, set_password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_category = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.Text, nullable=False)
    owned_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    bought_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    images = db.relationship("Image", backref="product", lazy=True)

    def name(self):
        return self.product_name.capitalize()

    name = property(name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
