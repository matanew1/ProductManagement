# Product Management API

This project is a Flask-based Product Management API that interacts with Firebase Realtime Database for storing product information. Firebase Authentication is used for user registration and login. The API allows users to manage (create, retrieve, update, delete) their products securely.

## Features

- **User Registration**: Register a user using Firebase Authentication.
- **User Login**: Authenticate users using Firebase Authentication.
- **Product Upload**: Create and upload a product to Firebase Realtime Database.
- **Product Retrieval**: Retrieve all products or user-specific products.
- **Product Update**: Update product details for authenticated users.
- **Product Deletion**: Delete a product that belongs to an authenticated user.
- **Search Products**: Search products by keyword.
- **Category Filtering**: Retrieve products by category.

## Technologies Used

- **Flask**: Web framework for building the API.
- **Firebase Admin SDK**: For secure operations like managing Firebase Authentication and Realtime Database.
- **Pyrebase**: To integrate Firebase Authentication for user login.
- **Firebase Realtime Database**: To store and manage product and user data.
- **Firebase Authentication**: For user authentication.
