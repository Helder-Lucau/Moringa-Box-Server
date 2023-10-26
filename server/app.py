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

class RegistrationForm(FlaskForm):
    firstName = StringField('Lastname', validators=[DataRequired(),Length(min=4,max=255)])
    lastName = StringField('Lastname', validators=[DataRequired(),Length(min=4,max=255)])
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=255)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=255)])
    
class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        form = RegistrationForm(data=data)
        
        if form.validate():
            first_name = form.firstName.data
            last_name = form.lastName.data
            email = form.email.data
            password = form.password.data

            if User.query.filter(User.email == email).first() is not None:
                return {'message': 'Username already exists'}, 400
            
            new_user = User(firstname=first_name, lastname=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.id)

            return {
                'message': "User registered successfully",
                'access_token': access_token
            }, 201
        else:
            return {'message': 'Validation errors', 'errors': form.errors}, 400

api.add_resource(UserRegistrationResource, '/register')

class UserLogInResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return{'message':'email and password required'},400
        
        user = User.query.filter_by(username=email).first()
        if user and user.password == password:
            access_token= create_access_token(identity=user.id)
            return {'access token':access_token},200
        else:
            return {'message':'Invalid credentials'},401
        
api.add_resource(UserLogInResource,'/login')


if __name__ == '__main__':
    app.run(port=5555, debug=True)