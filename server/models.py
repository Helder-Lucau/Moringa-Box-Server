from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    folders = db.relationship('Folder', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class File(db.Model, SerializerMixin):
    __tablename__ = 'files'

    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_image = db.Column(db.String(255))
    file_type = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_image':self.file_image,
            'upload_date': self.upload_date,
            'user_id': self.user_id,
            'folder_id': self.folder_id
        }

class Folder(db.Model, SerializerMixin):
    __tablename__ = 'folders'
    
    folder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folder_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    parent_folder_id = db.Column(db.Integer)

    subfolders = db.relationship('Folder', backref=db.backref('parent', remote_side=[folder_id]))
    files = db.relationship('File', backref='folder', lazy=True)

    def serialize(self):
        return {
            'folder_id': self.folder_id,
            'folder_name': self.folder_name,
            'user_id': self.user_id,
            'parent_folder_id': self.parent_folder_id
        }
