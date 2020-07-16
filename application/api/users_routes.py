from flask import Blueprint, Response, request, json
from flask_login import login_user, logout_user
from application.models.user import User
from .error import Error

# Blueprint Configuration
api = Blueprint('users', __name__, url_prefix='/api/v1')

###########
## USERS ##
###########

@api.route('/users', methods=['GET', 'POST'])
def users():
    try:
        if request.method == 'GET':   
            users = User.objects()
            return Response(users.to_json(), mimetype='application/json', status=200)
        elif request.method == 'POST':
            data = request.json
            user = User.create(data)
            login_user(user)
            return Response(user.to_json(), mimetype='application/json', status=200)
    except Error as e: return error(str(e))

@api.route('/users/logout', methods=['POST'])
def logout():
    logout_user()
    return Response("", mimetype='application/json', status=200)

###########
## ERROR ##
###########

def error(message):
    response = {'Error': message }
    return Response(json.dumps(response), mimetype='application/json', status=400)