import random
from models import db, User, File, Folder
from app import app
from random import randint
from datetime import datetime



with app.app_context():
    db.create_all()

users_data = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123',
    },
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'password': 'secret123',
    },
        {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'password': 'password123',
    },
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'janesmith@example.com',
        'password': 'secret123',
    },
    {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice@example.com',
        'password': 'alicepass',
    },
    {
        'first_name': 'Bob',
        'last_name': 'Williams',
        'email': 'bob@example.com',
        'password': 'bobpass',
    },
    {
        'first_name': 'Emily',
        'last_name': 'Brown',
        'email': 'emily@example.com',
        'password': 'emilypass',
    },
    {
        'first_name': 'David',
        'last_name': 'Lee',
        'email': 'david@example.com',
        'password': 'davidpass',
    },
    {
        'first_name': 'Sophia',
        'last_name': 'Clark',
        'email': 'sophia@example.com',
        'password': 'sophiapass',
    },
    {
        'first_name': 'Michael',
        'last_name': 'Wilson',
        'email': 'michael@example.com',
        'password': 'michaelpass',
    },
    {
        'first_name': 'Olivia',
        'last_name': 'Thomas',
        'email': 'olivia@example.com',
        'password': 'oliviapass',
    },
    {
        'first_name': 'James',
        'last_name': 'Anderson',
        'email': 'james@example.com',
        'password': 'jamespass',
    }
    ]
   


for user_data in users_data:
    user = User(**user_data)
    db.session.add(user)



files_data = [
    {
        'file_name': 'file1.txt',
        'file_path': '/path/to/file1.txt',
        'file_type': 'text',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file2.txt',
        'file_path': '/path/to/file2.txt',
        'file_type': 'text',
        'user_id': 2,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
]
files_data == [
    {
        'file_name': 'file1.txt',
        'file_path': '/path/to/file1.txt',
        'file_type': 'text',
        'user_id': 1,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file2.txt',
        'file_path': '/path/to/file2.txt',
        'file_type': 'text',
        'user_id': 2,  
        'folder_id': 2,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file3.txt',
        'file_path': '/path/to/file3.txt',
        'file_type': 'text',
        'user_id': 3,  
        'folder_id': 3,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file4.txt',
        'file_path': '/path/to/file4.txt',
        'file_type': 'text',
        'user_id': 4, 
        'folder_id': 4, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file5.txt',
        'file_path': '/path/to/file5.txt',
        'file_type': 'text',
        'user_id': 5,  
        'folder_id': 5,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file6.txt',
        'file_path': '/path/to/file6.txt',
        'file_type': 'text',
        'user_id': 6,  
        'folder_id': 1,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file7.txt',
        'file_path': '/path/to/file7.txt',
        'file_type': 'text',
        'user_id': 7,  
        'folder_id': 2, 
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file8.txt',
        'file_path': '/path/to/file8.txt',
        'file_type': 'text',
        'user_id': 8, 
        'folder_id': 3,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file9.txt',
        'file_path': '/path/to/file9.txt',
        'file_type': 'text',
        'user_id': 9, 
        'folder_id': 4,  
        'upload_date': datetime.now(),
    },
    {
        'file_name': 'file10.txt',
        'file_path': '/path/to/file10.txt',
        'file_type': 'text',
        'user_id': 10,  
        'folder_id': 5,  
        'upload_date': datetime.now(),
    }
  
]

for file_data in files_data:
    file = File(**file_data)
    db.session.add(file)

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
folders_data ==[
    {
        'folder_name': 'Folder 1',
        'user_id': 1, 
        'parent_folder_id': None,  
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
        
  
]

for folder_data in folders_data:
    folder = Folder(**folder_data)
    db.session.add(folder)


db.session.commit()

print("Sample data inserted into the database.")
