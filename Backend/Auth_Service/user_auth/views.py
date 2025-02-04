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
# import requests

# Secret key for JWT (add this in settings.py)
SECRET_KEY = "dbncjdhfjen32678930oeijdfhncbveuiyuwe8srty890-plkjhgfr43wsxcvgyu89olmngt54edf7"

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_db"]
collection = db["users"]

@api_view(['POST'])
def signup(request):
    # data = json.loads(request.body)
    # print(data)
    # collection.insert_one(data)
    # username = data.get("username")
    # email = data.get("email")
    # password = data.get("password")
    
    # if User.objects.filter(username=username).exists():
    #     return JsonResponse({'error': 'Username already exists'}, status=400)
    
    # user = User.objects.create_user(username=username, email=email, password=password)
    # return JsonResponse({'message': 'User created successfully'})

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
            # existing_user = collection.find_one({"$or": [{"username": username}, {"email": email}]})
            # if existing_user:
            #     return JsonResponse({"error": "User with this username or email already exists"}, status=400)
            
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

            # Insert new user
            # collection.insert_one(data)
            return JsonResponse({"message": "User registered successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# @api_view(['POST'])
# def signin(request):
#     data = json.loads(request.body)
#     username = data.get("username")
#     password = data.get("password")
    
#     user = User.objects.filter(username=username).first()
#     if user and user.check_password(password):
#         refresh = RefreshToken.for_user(user)
#         return JsonResponse({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })
#     return JsonResponse({'error': 'Invalid credentials'}, status=401)

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

            # username = collection.findOne({ "email": email })
            username=user['username']
            print(username)
            # Generate JWT Token (expires in 1 hour)
            payload = {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return JsonResponse({"message": "Login successful", "token": token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



# SUMMARIZATION_SERVICE_URL = "http://127.0.0.1:8002"

# def get_user_summaries(request):
#     token = request.headers.get("Authorization")
    
#     if not token:
#         return JsonResponse({"error": "Token is missing"}, status=401)

#     headers = {"Authorization": token}
    
#     try:
#         response = requests.get(f"{SUMMARIZATION_SERVICE_URL}/summaries/", headers=headers)
#         return JsonResponse(response.json(), status=response.status_code)
#     except requests.RequestException:
#         return JsonResponse({"error": "Failed to connect to summarization service"}, status=500)
