from firebase_admin import auth, db
from app.utils.helpers import handle_exception
import pyrebase


class AuthService:
    firebase = pyrebase.initialize_app({
        "apiKey": "AIzaSyBlH3AbKqjX7jrT7ZUvug34MB2_MiRq0dU",
        "authDomain": "productmanagement-a2e14.firebaseapp.com",
        "databaseURL": "https://productmanagement-a2e14-default-rtdb.firebaseio.com",
        "projectId": "productmanagement-a2e14",
        "storageBucket": "productmanagement-a2e14.appspot.com",
        "messagingSenderId": "1033785289784",
        "appId": "1:1033785289784:web:7e4b8c7f1f9f7a5f4a4e6f",
        "measurementId": "G-2J1J6V5X6Z"
    })
    auth_pyrebase = firebase.auth()

    @staticmethod
    def register_user(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password are required", "status": 400}

        try:
            user = auth.create_user(email=email, password=password)
            db.reference(f'users/{user.uid}').set({'email': email})
            return {"message": "User registered successfully", "status": 201}
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password are required", "status": 400}

        try:
            user = AuthService.auth_pyrebase.sign_in_with_email_and_password(email, password)
            return {"message": "User logged in successfully", "user": user, "status": 200}
        except Exception as e:
            return handle_exception(e)
