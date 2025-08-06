from app import create_app, db
from app.models import *
from app.models.superuser import superuser

app = create_app()

with app.app_context():
    db.create_all()

    if not superuser.query.first():
        default_admin = superuser(username="admin", password="admin@123#")
        db.session.add(default_admin)
        db.session.commit()
        print("Default superuser created.")
    else:
        print("Superuser already exists.")


if __name__ == "__main__":
    app.run(debug=True)