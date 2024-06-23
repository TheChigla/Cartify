import os, requests
from cartify import app, db
from flask import render_template, request, flash, redirect, url_for, session, json
from cartify.forms import (
    RegisterForm,
    LoginForm,
    ProductForm,
    UpdateProductName,
    UpdateProductPrice,
    UpdateProductQuantity,
    UpdateProductCategory,
    UpdateProductDescription,
    ProductQuantityForm,
)
from cartify.models import User, Product, Image
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from wtforms.validators import NumberRange


@app.route("/")
def home():
    products = Product.query.all()

    res = requests.get('https://categories-api-dpno.onrender.com/api/categories')
    categories = json.loads(res.content)

    return render_template("index.html", products=products, categories=categories)


@app.route("/user")
@login_required
def user():
    if current_user.role == "admin":
        added_products = Product.query.filter_by(owned_user=current_user.id).all()
        return render_template("user.html", added_products=added_products)

    my_products = Product.query.filter_by(owned_user=current_user.id).all()

    return render_template("user.html", my_products=my_products)


@app.route("/user/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        profile_pic = form.profile_pic.data
        password = form.password.data

        condition = profile_pic and profile_pic.filename != ""
        if condition:
            profile_pic.save(
                os.path.join(
                    app.config["PROFILE_UPLOAD_FOLDER"],
                    f"{email}-{secure_filename(profile_pic.filename)}",
                )
            )

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            profile_pic=(
                f"{email}-{secure_filename(profile_pic.filename)}" if condition else ""
            ),
            password=password,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user=user)

        flash("User successfully registered", category="success")
        return redirect(url_for("user"))
    elif form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")

    if current_user.is_authenticated:
        return redirect(url_for("user"))
    else:
        return render_template("register.html", form=form)


@app.route("/user/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password=form.password.data):
            login_user(user=user)
            flash("User successfully logged in", category="success")
        elif user is None:
            flash("User does not exist", category="danger")
        elif user.check_password(password=form.password.data) == False:
            flash("Incorrect password", category="danger")
            return redirect(url_for("login"))

            return redirect(url_for("user"))
    elif request.method == "POST" and form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")

    if current_user.is_authenticated:
        return redirect(url_for("user"))
    else:
        return render_template("login.html", form=form)


@app.route("/user/logout")
def logout():
    logout_user()
    flash("User successfully logged out", category="success")

    return redirect(url_for("login"))


@app.route("/product/<int:product_id>")
def product(product_id):
    form = ProductQuantityForm()
    product = Product.query.get(product_id)
    images = Image.query.filter_by(product_id=product_id).all()
    related_products = Product.query.filter_by(
        product_category=product.product_category
    ).all()

    for image in images:
        print(image.image_path)

    if product is None:
        flash("Product does not exist", category="danger")
        return redirect(url_for("home"))

    return render_template(
        "single-product.html",
        product=product,
        images=images,
        form=form,
        related_products=related_products,
    )


@app.route("/products/<string:category>")
def category(category):
    products = Product.query.filter_by(product_category=category).all()

    if products is None:
        flash("No products found", category="danger")
        return redirect(url_for("category"))

    return render_template("category.html", products=products, category=category)


@app.route("/products/search", methods=["GET", "POST"])
def search():
    search = request.args.get("search")
    products = Product.query.filter(Product.product_name.ilike(f"%{search}%")).all()

    print(products)

    if len(products) == 0:
        flash("No products found", category="danger")
        return redirect(url_for("home"))

    return render_template("search.html", products=products, search=search)


@app.route("/product/add", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    role = current_user.role

    if role != "admin":
        flash("You are not authorized to add products", category="danger")
        return redirect(url_for("user"))

    if request.method == "POST" and form.validate_on_submit():
        product_name = form.product_name.data
        product_price = form.product_price.data
        product_category = form.product_category.data
        product_quantity = form.product_quantity.data
        product_description = form.product_description.data
        user = current_user.id

        product = Product(
            product_name=product_name,
            product_price=product_price,
            product_category=product_category,
            product_quantity=product_quantity,
            product_description=product_description,
            owned_user=user,
        )
        db.session.add(product)
        db.session.commit()

        if not os.path.exists(
            os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product_name)
        ):
            os.makedirs(os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product_name))

        for image in form.images.data:
            if image.filename == "":
                continue

            image.save(
                os.path.join(
                    app.config["PRODUCT_UPLOAD_FOLDER"],
                    f"{product_name}/{secure_filename(image.filename)}",
                )
            )

            image = Image(
                product_id=product.id,
                image_path=f"{secure_filename(image.filename)}",
            )
            db.session.add(image)
            db.session.commit()

        flash("Product successfully added", category="success")
        return redirect(url_for("user"))

    return render_template("add-product.html", form=form, title="Add")


@app.route("/product/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    role = current_user.role
    if role != "admin":
        flash("You are not authorized to add products", category="danger")
        return redirect(url_for("user"))

    product = Product.query.get(product_id)
    update_name_form = UpdateProductName()
    update_price_form = UpdateProductPrice()
    update_quantity_form = UpdateProductQuantity()
    update_category_form = UpdateProductCategory()
    update_description_form = UpdateProductDescription()

    if request.method == "POST" and update_name_form.validate_on_submit():
        product_name = update_name_form.product_name.data
        if os.path.exists(
            os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product.product_name)
        ):
            os.rename(
                os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product.product_name),
                os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product_name),
            )
        product.product_name = product_name
        db.session.commit()

        flash("Product name successfully updated", category="success")
        return redirect(url_for("user"))
    elif request.method == "POST" and update_price_form.validate_on_submit():
        product_price = update_price_form.product_price.data
        product.product_price = product_price
        db.session.commit()
        flash("Product price successfully updated", category="success")
        return redirect(url_for("user"))
    elif request.method == "POST" and update_quantity_form.validate_on_submit():
        product_quantity = update_quantity_form.product_quantity.data
        product.product_quantity = product_quantity
        db.session.commit()
        flash("Product quantity successfully updated", category="success")
        return redirect(url_for("user"))
    elif request.method == "POST" and update_category_form.validate_on_submit():
        product_category = update_category_form.product_category.data
        product.product_category = product_category
        db.session.commit()
        flash("Product category successfully updated", category="success")
        return redirect(url_for("user"))
    elif request.method == "POST" and update_description_form.validate_on_submit():
        product_description = update_description_form.product_description.data
        product.product_description = product_description
        db.session.commit()
        flash("Product description successfully updated", category="success")
        return redirect(url_for("user"))

    update_category_form.product_category.default = product.product_category
    update_category_form.process()

    update_description_form.product_description.default = product.product_description
    update_description_form.process()

    return render_template(
        "modify-product.html",
        product=product,
        update_name_form=update_name_form,
        update_price_form=update_price_form,
        update_quantity_form=update_quantity_form,
        update_category_form=update_category_form,
        update_description_form=update_description_form,
    )


@app.route("/product/delete/<int:product_id>")
@login_required
def delete_product(product_id):
    role = current_user.role
    if role != "admin":
        flash("You are not authorized to delete products", category="danger")
        return redirect(url_for("user"))

    product = Product.query.get(product_id)

    if os.path.exists(
        os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product.product_name)
    ):
        images = Image.query.filter_by(product_id=product_id).all()
        for image in images:
            os.remove(
                os.path.join(
                    app.config["PRODUCT_UPLOAD_FOLDER"],
                    f"{product.product_name}/{image.image_path}",
                )
            )

        os.rmdir(
            os.path.join(app.config["PRODUCT_UPLOAD_FOLDER"], product.product_name)
        )

    images = Image.query.filter_by(product_id=product_id).all()
    for image in images:
        db.session.delete(image)
        db.session.commit()

    db.session.delete(product)
    db.session.commit()

    flash("Product successfully deleted", category="success")
    return redirect(url_for("user"))


@app.route("/cart")
@login_required
def cart():
    return render_template("cart.html")


@app.route("/cart/add/<int:product_id>/<int:product_quantity>", methods=["GET", "POST"])
@login_required
def add_to_cart(product_id, product_quantity):
    product = Product.query.get(product_id)
    form = ProductQuantityForm()
    form.product_quantity.validators.append(NumberRange(max=product.product_quantity))

    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(
                url_for(
                    "add_to_cart",
                    product_id=product_id,
                    product_quantity=form.product_quantity.data,
                )
            )
        elif form.errors != {}:
            for err_msg in form.errors.values():
                flash(err_msg[0], category="danger")
                return redirect(url_for("product", product_id=product_id))

    if "cart" not in session:
        session["cart"] = []

    if product.product_quantity == 0:
        flash("Product is out of stock", category="danger")
        return redirect(url_for("cart", product_id=product_id))

    for item in session["cart"]:
        if (
            item["product_id"] == product_id
            and item["product_quantity"] != product_quantity
        ):
            item["product_quantity"] += product_quantity
            session.modified = True
            flash("Product quantity successfully updated", category="success")
            return redirect(url_for("cart"))
        else:
            flash("Product already exists in cart", category="danger")
            return redirect(url_for("cart"))

    session["cart"].append(
        {
            "product_image": Image.query.filter_by(product_id=product_id)
            .first()
            .image_path,
            "product_id": product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_quantity": product_quantity,
        }
    )
    flash("Product successfully added to cart", category="success")
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    if "cart" not in session or len(session["cart"]) == 0:
        flash("No products in cart", category="danger")
        return redirect(url_for("cart"))

    for item in session["cart"]:
        if item["product_id"] == product_id:
            session["cart"].remove(item)
            session.modified = True
            flash("Product successfully removed from cart", category="success")
            return redirect(url_for("cart"))

    flash("Product does not exist in cart", category="danger")
    return redirect(url_for("cart"))


@app.route("/cart/checkout")
@login_required
def checkout():
    total_price = 0

    if "cart" not in session or len(session["cart"]) == 0:
        flash("No products in cart", category="danger")
        return redirect(url_for("cart"))

    for item in session["cart"]:
        total_price = item["product_price"] * item["product_quantity"]

    if current_user.budget < total_price:
        flash("Insufficient funds", category="danger")
        return redirect(url_for("cart"))

    product = Product.query.get(item["product_id"])
    product.product_quantity -= item["product_quantity"]
    product.owned_user = current_user.id
    current_user.budget -= total_price

    db.session.commit()

    session.pop("cart", None)
    session.modified = True
    flash("Products successfully checked out", category="success")

    return redirect(url_for("user"))
