
# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from django.contrib.auth import login as django_login
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import Users
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests





class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']

            user = authenticate(request, identifier=identifier, password=password)

            if user:
                login(request, user)
                user_data = UserSerializer(user).data
                return Response({'message': 'Login successful', 'user': user_data})
            else:
                return Response({'non_field_errors': ['Unable to log in with provided credentials.']},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def google_login(request):
    token = request.POST.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1064045400562-lljdlndc03j31gh3e3njeegd4p79ms4l.apps.googleusercontent.com")

        user_email = idinfo['email']
        user_name = idinfo['name']
        # Handle user login / creation here

    except ValueError:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    


@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out"})
    return JsonResponse({"error": "Method not allowed"}, status=405)



# class LogoutView(APIView):
#     def post(self, request):
#         logout(request)  # Clears the session
#         return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    







# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')
#             user = authenticate(request, email=email, password=password )
#             if user:
#                 user_data = UserSerializer(user).data
#                 return Response({'message': 'Login successful', 'user': user_data})
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


