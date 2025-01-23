from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from .db import MongoDB
from .auth import JWTAuth
import json
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Income
from .serializers import IncomeSerializer

mongo_db = MongoDB()

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        
        if mongo_db.email_exists(email):
            return Response(
                {'error': 'Email already registered'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        
        hashed_password = make_password(serializer.validated_data['password'])
        user = mongo_db.create_user(
            email=email,
            username=serializer.validated_data['username'],
            hashed_password=hashed_password
        )

        
        tokens = JWTAuth.create_token(user['_id'])

        return Response({
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'username': user['username']
            },
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Please provide email and password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = mongo_db.get_user_by_email(email)
    
    if not user or not check_password(password, user['password']):
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    tokens = JWTAuth.create_token(user['_id'])

    return Response({
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'username': user['username']
        },
        'tokens': tokens
    })
class IncomeListCreateView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_class = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_query(self):
        return self.queryset.filter(user=self.request.user)
class IncomeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_class = [IsAuthenticated] 

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)