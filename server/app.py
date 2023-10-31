from flask import Flask, jsonify, request, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource,reqparse, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.datastructures import FileStorage
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email 
from datetime import datetime
from models import db, User, File, Folder
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

current_directory = os.getcwd()  
app.config['UPLOAD_FOLDER'] = os.path.join(current_directory, 'uploads')


app.config['WTF_CSRF_ENABLED'] = False

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moringa_box.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False
1
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

class FolderListResource(Resource):
    # @jwt_required()
    def get(self):
        folders = Folder.query.all()
        folder_list = [{'folder_id': folder.folder_id, 'folder_name': folder.folder_name} for folder in folders]
        return {'folders': folder_list}, 200

class FolderUploadResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('folder_name', type=str, required=True)
        parser.add_argument('parent_folder_id', type=int)  

        args = parser.parse_args()
        folder_name = args['folder_name']
        current_user_id = get_jwt_identity()
        parent_folder_id = args.get('parent_folder_id')

        new_folder = Folder(
            folder_name=folder_name,
            user_id=current_user_id,
            parent_folder_id=parent_folder_id,  
        )
        db.session.add(new_folder)
        db.session.commit()

        return {'message': 'Folder uploaded successfully'}, 200

class FolderResource(Resource):
    @jwt_required()
    def delete(self, folder_id):
        folder_to_delete = Folder.query.get(folder_id)
        if folder_to_delete:
            
            files_in_folder = File.query.filter_by(folder_id=folder_id).all()
            for file in files_in_folder:
                db.session.delete(file)

            db.session.delete(folder_to_delete)
            db.session.commit()
            return {'message': f'Folder {folder_id} deleted successfully'}, 200
        return {'message': f'Folder {folder_id} not found'}, 404

api.add_resource(FolderListResource, '/folders')
api.add_resource(FolderUploadResource, '/upload_folder')
api.add_resource(FolderResource, '/folder/<int:folder_id>')

class FileListResource(Resource):
    # @jwt_required()
    def get(self):
        files = File.query.all()
        file_list = [file.serialize() for file in files]
        return jsonify({'files': file_list})

class FileUploadResource(Resource):
    @jwt_required()
    def post(self):

        current_user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files')
        parser.add_argument('file_name', type=str, required=True)
        parser.add_argument('file_type', type=str, required=True)
        parser.add_argument('file_image', type=str)
        parser.add_argument('folder_id', type=int, required=True)  

        args = parser.parse_args()
        uploaded_file = args['file']
        file_name = args['file_name']
        file_type = args['file_type']
        file_image = args['file_image']
        folder_id = args['folder_id'] 

        if uploaded_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            uploaded_file.save(file_path)

            folder = Folder.query.filter_by(folder_id=folder_id).first()

            if folder:
                new_file = File(
                    file_name=file_name,
                    file_path=file_path,
                    file_type=file_type,
                    file_image=file_image,
                    upload_date=datetime.now(),
                    user_id=current_user_id,
                    folder_id=folder_id  
                )
                db.session.add(new_file)
                db.session.commit()

                return jsonify({'message': 'File uploaded successfully'})
            else:
                return jsonify({'message': 'Invalid folder ID'}), 400

        return jsonify({'message': 'No file found in the request'})

class FileDownloadResource(Resource):
    @jwt_required()
    def get(self, file_id):
        file = db.session.get(File, file_id)
        if file:
            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=file.file_path, as_attachment=True)
        return jsonify({'message': 'File not found'}), 404

class FileDeleteResource(Resource):
    @jwt_required()
    def delete(self, file_id):
        file = File.query.get(file_id)
        if file:
            db.session.delete(file)
            db.session.commit()
            return jsonify({'message': f'File {file_id} deleted successfully'}), 200
        else:
            abort(404, message="File not found")

api.add_resource(FileListResource, '/files')
api.add_resource(FileUploadResource, '/upload')
api.add_resource(FileDownloadResource, '/download/<int:file_id>')
api.add_resource(FileDeleteResource, '/file/<int:file_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)