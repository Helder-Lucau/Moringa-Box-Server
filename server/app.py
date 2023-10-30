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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa_box.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)
api = Api(app)

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired(),Length(min=4,max=100)])
    lastname = StringField('Lastname', validators=[DataRequired(),Length(min=4,max=100)])
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=100)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    
class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        form = RegistrationForm(data=data)
        
        if form.validate():
            first_name = form.firstname.data
            last_name = form.lastname.data
            email = form.email.data
            password = form.password.data

            if User.query.filter(User.email == email).first() is not None:
                return {'message': 'Email already exists'}, 400
            
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.user_id)

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
            return{'message':'Email and password required'},400
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            access_token= create_access_token(identity=user.user_id)
            return {'access token':access_token},200
        else:
            return {'message':'Invalid credentials'},401
        
api.add_resource(UserLogInResource,'/login')


if __name__ == '__main__':
    app.run(port=5555, debug=True)