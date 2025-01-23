from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from .db import MongoDB
from .auth import JWTAuth
import json
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
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

class IncomeListCreateView(generics.GenericAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = str(request.user.id)
        incomes = mongo_db.get_incomes_by_user(user_id)
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = str(request.user.id)
        income = mongo_db.create_income(
            user_id=user_id,
            amount=serializer.validated_data['amount'],
            description=serializer.validated_data['description'],
            date=serializer.validated_data['date']
        )
        return Response(income, status=status.HTTP_201_CREATED)

class IncomeDetailView(generics.GenericAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        income_id = kwargs.get('pk')
        income = mongo_db.get_income_by_id(income_id)
        if not income:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(income)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        income_id = kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = mongo_db.update_income(
            income_id=income_id,
            amount=serializer.validated_data['amount'],
            description=serializer.validated_data['description'],
            date=serializer.validated_data['date']
        )
        if not updated:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        income_id = kwargs.get('pk')
        deleted = mongo_db.delete_income(income_id)
        if not deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
