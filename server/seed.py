from models import db, User, File, Folder
from app import app
from random import randint
from datetime import datetime

# Create an application context
with app.app_context():
    db.session.query(User).delete()
    db.session.query(File).delete()
    db.session.query(Folder).delete()

    db.create_all()

    # Seed user data
    users_data = [
    {
        'first_name': 'Linda',
        'last_name': 'Wambui',
        'email': 'lindawambui@gmail.com',
        'password': 'linda023',
    },
    {
        'first_name': 'Evans',
        'last_name': 'Miranda',
        'email': 'evansmiranda@gmail.com',
        'password': 'miranda1',
    },
    {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice@gmail.com',
        'password': 'alicepass',
    },
    {
        'first_name': 'Bob',
        'last_name': 'Williams',
        'email': 'bob@gmail.com',
        'password': 'bob4',
    },
    {
        'first_name': 'Emily',
        'last_name': 'Brown',
        'email': 'emily@gmail.com',
        'password': 'emilypass',
    },
    {
        'first_name': 'David',
        'last_name': 'Lee',
        'email': 'david@gmail.com',
        'password': 'davidlee45',
    },
    {
        'first_name': 'Sophia',
        'last_name': 'Clark',
        'email': 'sophia@gmail.com',
        'password': 'sophia9',
    },
    {
        'first_name': 'Michael',
        'last_name': 'Wilson',
        'email': 'michael@gmail.com',
        'password': 'wilson89',
    },
    {
        'first_name': 'Olivia',
        'last_name': 'Thomas',
        'email': 'olivia@gmail.com',
        'password': 'oliviaT23',
    },
    {
        'first_name': 'James',
        'last_name': 'Anderson',
        'email': 'james@gmail.com',
        'password': 'james34',
    }
 ]
 
    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)

    # Seed file data
    files_data = [
    {
        'file_name': 'travel_guide.pdf',
        'file_path': '/path/to/travel_guide.pdf',
        'file_image':'',
        'file_type': 'pdf',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'assignment.pdf',
        'file_path': '/path/to/assignment.pdf',
        'file_image':'',
        'file_type': 'pdf',
        'user_id': 2,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'note.txt',
        'file_path': '/path/to/note.txt',
        'file_image':'',
        'file_type': 'text',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'resume.pdf',
        'file_path': '/path/to/resume.pdf',
        'file_image':'',
        'file_type': 'pdf',
        'user_id': 10,  
        'folder_id': 5,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'dog.jpg',
        'file_path': '/path/to/dog.jpg',
        'file_image':'',
        'file_type': 'jpg',
        'user_id': 3,  
        'folder_id': 3,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'report.docx',
        'file_path': '/path/to/report.docx',
        'file_image':'',
        'file_type': 'docx',
        'user_id': 9, 
        'folder_id': 4, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'letter.docx',
        'file_path': '/path/to/letter.docx',
        'file_image':'',
        'file_type': 'docx',
        'user_id': 5,  
        'folder_id': 5,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'essay.pdf',
        'file_path': '/path/to/essay.pdf',
        'file_image':'',
        'file_type': 'pdf',
        'user_id': 6,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'react.jpg',
        'file_path': '/path/to/react.jpg',
        'file_image':'',
        'file_type': 'jpg',
        'user_id': 7,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'story.txt',
        'file_path': '/path/to/story.txt',
        'file_image':'',
        'file_type': 'text',
        'user_id': 8, 
        'folder_id': 3,  
        'upload_date': datetime.now(),
    },
 ]
    
    for file_data in files_data:
        file = File(**file_data)
        db.session.add(file)

    # Seed folder data
    folders_data = [
    {
        'folder_name': 'Folder 1',
        'user_id': 1, 
        'parent_folder_id': None, 
    },
    {
        'folder_name': 'Folder 2',
        'user_id': 1, 
        'parent_folder_id': None,  
    },
    {
        'folder_name': 'Subfolder 1',
        'user_id': 2, 
        'parent_folder_id': 2,  
    },
    {
        'folder_name': 'Folder 2',
        'user_id': 2,  
        'parent_folder_id': None, 
    },
    {
        'folder_name': 'Folder 3',
        'user_id': 3,  
        'parent_folder_id': None,  
    },
    {
        'folder_name': 'Subfolder 1',
        'user_id': 1, 
        'parent_folder_id': 1, 
    },
 ]

    for folder_data in folders_data:
        folder = Folder(**folder_data)
        db.session.add(folder)

    db.session.commit()

print("Seeded data successfully.")
