# Moringa Box API
# File Management System API

This Flask-based API provides endpoints to manage users, folders, and files in a file management system. Users can register, log in, create folders, upload files, and manage their files and folders through the provided API endpoints.

## Prerequisites

Make sure you have the following installed:

- Python (>=3.6)
- Flask
- Flask-Migrate
- Flask-CORS
- Flask-RESTful
- Flask-JWT-Extended
- Flask-WTF
- SQLAlchemy

You can install the required packages using the following command:


## How to Run

1. Clone this repository:
bash
git clone https://github.com/Helder-Lucau/Moringa-Box-Server


2. Set up the Flask application:
python
export FLASK_APP=moringabox/api/app/main.py
export FLASK_APP=app.py
export FLASK_ENV=development


3. Initialize the database:
flask db init
flask db migrate
flask db upgrade

4. Run the Flask application:
flask run


The API server will start running on `http://localhost:5555`.

## API Endpoints

- **POST /register**: Register a new user. Required fields: `firstname`, `lastname`, `email`, `password`.

- **POST /login**: Log in an existing user. Required fields: `email`, `password`.

- **GET /folders**: Get a list of all folders.

- **POST /upload_folder**: Upload a new folder. Required fields: `folder_name`, `parent_folder_id` (optional).

- **DELETE /folder/{folder_id}**: Delete a folder by ID.

- **GET /files**: Get a list of all files.

- **POST /upload**: Upload a new file. Required fields: `file` (file upload), `file_name`, `file_type`, `file_image`, `folder_id`.

- **GET /download/{file_id}**: Download a file by ID.

- **DELETE /file/{file_id}**: Delete a file by ID.

## Database Models

### User

- `user_id`: Integer (Primary Key)
- `first_name`: String (255), Not Null
- `last_name`: String (255), Not Null
- `email`: String (255), Unique, Not Null
- `password`: String (255), Not Null

### File

- `file_id`: Integer (Primary Key)
- `file_name`: String (255), Not Null
- `file_path`: String (255), Not Null
- `file_image`: String (255)
- `file_type`: String (255), Not Null
- `user_id`: Integer (Foreign Key, Users)
- `folder_id`: Integer (Foreign Key, Folders)
- `upload_date`: DateTime, Not Null

### Folder

- `folder_id`: Integer (Primary Key)
- `folder_name`: String (255), Not Null
- `user_id`: Integer (Foreign Key, Users)
- `parent_folder_id`: Integer (Foreign Key, Folders)

## Sample Data

The API is pre-populated with sample user data, folders, and files. You can use these sample data for testing the endpoints.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


