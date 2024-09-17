import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    cred = credentials.Certificate('app/models/secret.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://productmanagement-a2e14-default-rtdb.firebaseio.com/'
    })


initialize_firebase()
