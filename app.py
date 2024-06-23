from cartify import app, db
from os import path

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
