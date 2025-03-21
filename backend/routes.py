from flask import Blueprint
from extend import db
from models import User

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/add_user/<name>')
def add_user(name):
    try:
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return f"User '{name}' added successfully!"
    except Exception as e:
        db.session.rollback()
        return f"Failed to add user: {str(e)}"

@app_routes.route('/users')
def get_users():
    users = User.query.all()
    return {'users': [user.name for user in users]}
