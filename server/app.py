from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email 
from datetime import datetime
from models import db, User, File, Folder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'


app.config['WTF_CSRF_ENABLED'] = False

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moringa_box_db_user:S3Yg6LuOyiinvffLP4Y7MMuXx9vbZDAj@dpg-ckta8co168ec73bopsfg-a.oregon-postgresql.render.com/moringa_box_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)
api = Api(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)