from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
import json
import pymongo
import bcrypt
import jwt
import datetime
from django.conf import settings
from django.middleware.csrf import get_token
from django.views import View
from rest_framework.permissions import IsAuthenticated
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get values from .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]
collection2 = db['videos']

@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract user details
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Check for missing fields
            if not username or not email or not password:
                return JsonResponse({"error": "Username, email, and password are required"}, status=400)
            
            # Check if user already exists
            existing_user = collection.find_one({"email": email})
            if existing_user:
                return JsonResponse({"error": "User with this email already exists"}, status=400)
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Insert new user with hashed password
            collection.insert_one({
                "username": username,
                "email": email,
                "password": hashed_password.decode("utf-8")  # Store as a string
            })

            return JsonResponse({"message": "User registered successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(['POST'])
def signin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract login details
            email = data.get("email")
            password = data.get("password")

            # Check for missing fields
            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            # Find user in database
            user = collection.find_one({"email": email})
            if not user:
                return JsonResponse({"error": "User not found please check the email is valid"}, status=401)

            # Verify the password
            if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                return JsonResponse({"error": "Incorrect password"}, status=401)

            username=user['username']
            # Generate JWT Token (expires in 1 hour)
            payload = {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            return JsonResponse({"message": "Login successful", "token": token, "username":username}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(['POST'])
def getUserdetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)            
            name = data.get("username")
            res = collection.find_one({"username": name})
            
            if res:
                # Convert ObjectId to string
                res['_id'] = str(res['_id'])
                return JsonResponse(res, safe=False)
            else:
                return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error":"Invalid Json data"},status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(['PUT'])
def updatePassword(request):
    if request.method == 'PUT':
        try:
            # Get data from the request
            data = json.loads(request.body)
            username = data.get("username")
            oldPassword = data.get("oldPassword")
            newPassword = data.get("newPassword")

            # Fetch the user data from the database
            user = collection.find_one({"username": username})
            if user:
                # Retrieve stored hashed password
                stored_password = user.get("password")
                # Compare old password with the hashed password from the database
                if bcrypt.checkpw(oldPassword.encode('utf-8'), stored_password.encode('utf-8')):
                    # Hash the new password
                    hashed_new_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())

                    # Update the password in the database
                    collection.update_one({"username": username}, {"$set": {"password": hashed_new_password.decode('utf-8')}})

                    return JsonResponse({"message": "Password updated successfully"}, status=200)
                else:
                    return JsonResponse({"error": "Old password is incorrect"}, status=400)
            else:
                return JsonResponse({"error": "User not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(['POST'])
def getVideoDetials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)            
            name = data.get("username")
            print(name)
            results = collection2.find({"user": name})
            
            if results:
                # Convert ObjectId to string and create a list of results
                response_data = []
                for res in results:
                    res['_id'] = str(res['_id'])  # Convert ObjectId to string
                    response_data.append(res)
                return JsonResponse(response_data, safe=False, status=200)
            else:
                return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error":"Invalid Json data"},status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)