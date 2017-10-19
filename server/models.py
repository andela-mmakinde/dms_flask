from werkzeug.security import generate_password_hash, check_password_hash

from server import db

class User(db.Model):
    """
    Create a User table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    fullName = db.Column(db.String(60), index=True, unique=False)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'), default=6)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    documents = db.relationship('Document', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.fullName)

class Document(db.Model):
    """
    Create a Document table
    """
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    access = db.Column(db.String(60))
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'))
    ownerId = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(200))

    def __init__(self, title, access, content, ownerId, roleId):
        """initialize with name."""
        self.title = title
        self.access = access
        self.content = content
        self.ownerId = ownerId
        self.roleId = roleId


    def __repr__(self):
        return '<Department: {}>'.format(self.title)

class Role(db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    documents = db.relationship('Document', backref='role', lazy='dynamic')

    def __init__(self, title):
        """initialize with name."""
        self.title = title

    def __repr__(self):
        return '<Role: {}>'.format(self.title)
