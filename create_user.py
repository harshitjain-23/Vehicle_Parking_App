from app import db
from app.models.superuser import superuser

new_admin = superuser(username="admin", password="admin123")
db.session.add(new_admin)
db.session.commit()
