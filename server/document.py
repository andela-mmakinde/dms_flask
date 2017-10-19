# import os
# from flask import request, jsonify, abort
# from server import create_app, db
# from server.models import User, Role, Document

# config_name = os.getenv('FLASK_CONFIG')

# app = create_app(config_name)


# @app.route('/documents', methods=['POST'])
# def create_document():
#   document = Document(
#     title=str(request.form.get('title')),
#     access=str(request.form.get('access')),
#     content=str(request.form.get('content')),
#     roleId=(request.form.get('roleId')),
#     ownerId=(request.form.get('ownerId')))

#   db.session.add(document)
#   db.session.commit()
#   response = jsonify({ "success": "document saved successfully" })
#   response.status_code = 201

#   return response


