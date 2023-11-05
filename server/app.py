from flask import Flask, jsonify, request, send_file, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource,reqparse, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email 
from datetime import datetime
from models import db, User, File, Folder
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

# Set up the UPLOAD_FOLDER
current_directory = os.getcwd()  
UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')

# Check if the UPLOAD_FOLDER exists, if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['WTF_CSRF_ENABLED'] = False

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moringa_box_db_qidb_user:3swdbhjUbl6EE6cr9Sj71iDALYdDHITW@dpg-cl32o2ot3kic73d63220-a.oregon-postgres.render.com/moringa_box_db_qidb'
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

class FolderDeleteResource(Resource):
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
    
class FolderContentsResource(Resource):
    @jwt_required()
    def get(self, folder_id):
        folder = Folder.query.get(folder_id)
        if folder:
            files = File.query.filter_by(folder_id=folder_id).all()
            file_list = [{'file_id': file.file_id, 'file_name': file.file_name} for file in files]
            return {'folder_id': folder_id, 'folder_name': folder.folder_name, 'files': file_list}, 200
        return {'message': f'Folder {folder_id} not found'}, 404


api.add_resource(FolderContentsResource, '/folder-contents/<int:folder_id>')
api.add_resource(FolderListResource, '/folders')
api.add_resource(FolderUploadResource, '/upload-folder')
api.add_resource(FolderDeleteResource, '/folder/<int:folder_id>')

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

        if request.content_type != 'application/json':
            uploaded_file = request.files.get('file')
            folder_id = request.form.get('folder_id') 

            if uploaded_file:
                file_name = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                uploaded_file.save(file_path)

                file_type = file_name.rsplit('.', 1)[1].lower()

                new_file = File(
                    file_name=file_name,
                    file_path=file_path,
                    file_type=file_type,
                    upload_date=datetime.now(),
                    user_id=current_user_id,
                    folder_id=folder_id if folder_id else None 
                )

                uploaded_image = request.files.get('file_image')
                if uploaded_image:
                    file_image_name = secure_filename(uploaded_image.filename)
                    file_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file_image_name)
                    uploaded_image.save(file_image_path)
                    new_file.file_image = file_image_path

                db.session.add(new_file)
                db.session.commit()

                return jsonify({'message': 'File uploaded successfully'})
            else:
                return jsonify({'message': 'No file found in the request'})

        return jsonify({'message': 'Expected a different content type'})

class FileUploadInFolderResource(Resource):
    @jwt_required()
    def post(self, folder_id):
        current_user_id = get_jwt_identity()

        folder = Folder.query.filter_by(folder_id=folder_id).first()
        if not folder:
            return make_response(jsonify({'message': 'Invalid folder ID'}), 400)

        if request.content_type != 'application/json':
            uploaded_file = request.files.get('file')

            if uploaded_file:
                file_name = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                uploaded_file.save(file_path)

                file_type = file_name.rsplit('.', 1)[1].lower()

                new_file = File(
                    file_name=file_name,
                    file_path=file_path,
                    file_type=file_type,
                    upload_date=datetime.now(),
                    user_id=current_user_id,
                    folder_id=folder_id
                )

                uploaded_image = request.files.get('file_image')
                if uploaded_image:
                    file_image_name = secure_filename(uploaded_image.filename)
                    file_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file_image_name)
                    uploaded_image.save(file_image_path)
                    new_file.file_image = file_image_path

                db.session.add(new_file)
                db.session.commit()

                return jsonify({'message': 'File uploaded successfully'})
            else:
                return jsonify({'message': 'No file found in the request'})

        return jsonify({'message': 'Expected a different content type'})

class FileImageResource(Resource):
    def get(self, file_id):
        file = File.query.filter_by(file_id=file_id).first()

        if file:
            image_path = file.file_image
            return send_file(image_path)
        else:
            return make_response(jsonify({'message': 'File not found'}), 404)

class FileDownloadResource(Resource):
    @jwt_required()
    def get(self, file_id):
        file = File.query.filter_by(file_id=file_id).first()
        if file:
            return send_file(file.file_path, as_attachment=True)
        else:
            return make_response(jsonify({'message': 'File not found'}), 404)
        
class FileDeleteResource(Resource):
    @jwt_required()
    def delete(self, file_id):
        file = File.query.get(file_id)
        if file:
            db.session.delete(file)
            db.session.commit()
            return make_response(jsonify({'message': f'File {file_id} deleted successfully'}), 200)
        else:
            abort(404, message="File not found")
            
class MoveFileResource(Resource):
    @jwt_required()
    def put(self, file_id, new_folder_id):
        file_to_move = File.query.get(file_id)
        destination_folder = Folder.query.get(new_folder_id)

        if file_to_move:
            if destination_folder:
                file_to_move.folder_id = new_folder_id
                db.session.commit()
                return {'message': f'File {file_id} moved to folder {new_folder_id}'}, 200
            else:
                return {'message': f'Destination folder {new_folder_id} does not exist'}, 404
        else:
            return {'message': f'File {file_id} not found'}, 404

api.add_resource(MoveFileResource, '/move-file/<int:file_id>/<int:new_folder_id>')           
api.add_resource(FileListResource, '/files')
api.add_resource(FileDownloadResource, '/download/<int:file_id>')
api.add_resource(FileUploadResource, '/upload')
api.add_resource(FileUploadInFolderResource, '/upload/<int:folder_id>')
api.add_resource(FileDeleteResource, '/file/<int:file_id>')
api.add_resource(FileImageResource, '/file-image/<int:file_id>') 

if __name__ == '__main__':
    app.run(port=5555, debug=True)