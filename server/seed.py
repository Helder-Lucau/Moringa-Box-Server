sample_users = [
    {
        'first_name': 'Lacy',
        'last_name': 'Helmer',
        'username': 'lacy.hel',
        'email': 'lacy@yahoo.com',
        'password': 'h728827290',
    },
    {
        'first_name': 'Killmal',
        'last_name': 'Jonte',
        'username': 'jonte.him',
        'email': 'jonte@yahoo.com',
        'password': 'secret123',
    },
    {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'username': 'alicej',
        'email': 'alice@yahoo.com',
        'password': 'alicepass',
    },
]

user = User(**user_data)
db.session.add(user)
db.session.commit()

print("Sample users inserted into the database.")

