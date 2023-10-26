from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringabox_database.db' 
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.column(db.String(255))

    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    folders = db.relationship('Folder', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)

class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    file_type = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.folder_id'))
    upload_date = db.Column(db.DateTime)

class Folder(db.Model):
    folder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folder_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    parent_folder_id = db.Column(db.Integer)
    subfolders = db.relationship('Folder', backref=db.backref('parent', remote_side=[folder_id]))
    files = db.relationship('File', backref='folder', lazy=True)

if __name__ == '__main__':
    db.create_all()
