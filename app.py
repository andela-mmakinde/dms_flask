import os
from flask import request, jsonify, abort
from server import create_app, db
from server.models import User, Role, Document

config_name = os.getenv('FLASK_CONFIG')

app = create_app(config_name)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to Document Manager"})


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    user = User(
        email=str(request.form.get('email')),
        fullName=str(request.form.get('fullName')),
        password=str(request.form.get('password')),
        roleId=str(request.form.get('roleId', 6)))
    db.session.add(user)
    db.session.commit()
    response = jsonify({"success": "user details saved successfully"})
    response.status_code = 201
    return response


@app.route('/api/v1/users/login', methods=['POST'])
def login():
    email = str(request.form.get('email'))
    user = User.query.filter_by(email=email).first()
    if not user:
        response = jsonify({
          "message": "user record not found"
        })
        response.status_code = 404
        return response
    confirm_password = user.verify_password(password=str(request.form.get('password')))
    if confirm_password:
      response = jsonify({"message": "Logged in!"})
      response.status_code = 200
      return response

@app.route('/api/v1/users/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out!"})
    response.status_code = 200
    return response


@app.route('/api/v1/users/search/', methods=['GET'], strict_slashes=False)
def search_user():
    query = request.args.get('q')
    users = User.query.filter(User.email.like("%" + query + "%")).all()
    results = []
    for user in users:
        obj = {
            'id': user.id,
            'email': user.email,
            'password': user.password_hash,
        }
        results.append(obj)
    response = jsonify({
        "status": "success",
        "user": results
    })
    response.status_code = 200
    return response


@app.route('/api/v1/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id(id, **kwargs):
    user = User.query.filter_by(id=id).first()
    if not user:
        response = jsonify({
            "message": "user not found"
        })
        response.status_code = 404
        return response

    if request.method == 'GET':
        response = jsonify({
            'id': user.id,
            'email': user.email,
            'password': user.password_hash,
        })
        response.status_code = 200
        return response

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        response = jsonify({
            "message": "user deleted successfully"
        })
        response.status_code = 200
        return response

    elif request.method == 'PUT':
        fullName = str(request.form.get('fullName', user.fullName))
        email = str(request.form.get('email', user.email))
        password = str(request.form.get('password', ''))
        roleId = request.form.get('roleId')
        user.fullName = fullName
        user.email = email
        user.password = password
        user.roleId = roleId
        db.session.add(user)
        db.session.commit()
        response = jsonify({'message': "role updated successfully"})
        response.status_code = 200
        return response


@app.route('/api/v1/documents', methods=['GET', 'POST'])
def documents():
    if request.method == 'POST':
        document = Document(
            title=str(request.form.get('title')),
            access=str(request.form.get('access')),
            content=str(request.form.get('content')),
            roleId=(request.form.get('roleId')),
            ownerId=(request.form.get('ownerId')))
        db.session.add(document)
        db.session.commit()
        response = jsonify({"success": "document saved successfully"})
        response.status_code = 201

        return response


@app.route('/api/v1/roles', methods=['POST', 'GET'])
def create_role():
    if request.method == 'POST':
        title = str(request.form.get('title', ' '))
        role = Role(title=title)
        db.session.add(role)
        db.session.commit()
        response = jsonify({
            'status': 'Role created successfully',
            'role': role.title
        })
        response.status_code = 201
        return response
    elif request.method == 'GET':
        roles = Role.query.all()
        results = []
        for role in roles:
            obj = {
                'id': role.id,
                'title': role.title,
            }
            results.append(obj)
        response = jsonify({
            'status': 'success',
            'role': results
        })
        response.status_code = 200
        return response


@app.route('/api/v1/roles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def roles_by_id(id, **kwargs):
    role = Role.query.filter_by(id=id).first()
    if not role:
        response = jsonify({
            "message": "role not found"
        })
        response.status_code = 404
        return response

    if request.method == 'GET':
        response = jsonify({
            'id': role.id,
            'title': role.title,
        })
        response.status_code = 200
        return response

    elif request.method == 'DELETE':
        db.session.delete(role)
        db.session.commit()
        response = jsonify({"message": "role deleted successfully"})
        response.status_code
        return response

    elif request.method == 'PUT':
        title = str(request.form.get('title', ' '))
        role.title = title
        db.session.add(role)
        db.session.commit()
        response = jsonify({'message': "role updated successfully"})
        response.status_code = 200
        return response


if __name__ == '__main__':
    app.run()
