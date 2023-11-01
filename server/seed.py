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
        'file_image':'https://images.unsplash.com/photo-1615318201878-e3499973e9dc?auto=format&fit=crop&q=80&w=1887&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'pdf',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'assignment.pdf',
        'file_path': '/path/to/assignment.pdf',
        'file_image':'https://images.unsplash.com/photo-1562654501-a0ccc0fc3fb1?auto=format&fit=crop&q=80&w=1932&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'pdf',
        'user_id': 2,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'note.txt',
        'file_path': '/path/to/note.txt',
        'file_image':'https://plus.unsplash.com/premium_photo-1684772692884-9094d7ba083f?auto=format&fit=crop&q=80&w=1917&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'text',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'resume.pdf',
        'file_path': '/path/to/resume.pdf',
        'file_image':'https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=2070&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
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
        'file_image':'https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?auto=format&fit=crop&q=80&w=1888&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'docx',
        'user_id': 9, 
        'folder_id': 4, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'letter.docx',
        'file_path': '/path/to/letter.docx',
        'file_image':'https://images.unsplash.com/photo-1594320207823-405209d4a92b?auto=format&fit=crop&q=80&w=1925&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'docx',
        'user_id': 5,  
        'folder_id': 5,  
        'upload_date': datetime.now(),
    },
    {
        
        'file_name': 'essay.pdf',
        'file_path': '/path/to/essay.pdf',
        'file_image':'https://images.unsplash.com/photo-1504691342899-4d92b50853e1?auto=format&fit=crop&q=80&w=2070&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'pdf',
        'user_id': 6,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'react.jpg',
        'file_path': '/path/to/react.jpg',
        'file_image':'https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&q=80&w=2070&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'file_type': 'jpg',
        'user_id': 7,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'story.txt',
        'file_path': '/path/to/story.txt',
        'file_image':'https://images.unsplash.com/photo-1519791883288-dc8bd696e667?auto=format&fit=crop&q=80&w=2070&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
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
