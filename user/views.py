from django.shortcuts import render

from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from apps.configuration.models import Book,State
from .models import UserDetails

from .serializers import UserDetailSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


from django.contrib import auth





class UserDetail(CreateAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                user_details = UserDetails.objects.get(user=user)
                if user_details:
                	serializer = UserDetailSerializer(user_details)

                else:
                	serializer = UserSerializer(user)

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                message = 'Login Successfull'
                context = {'success': True, 'message': message, 'token': token, 'error': '', 'data': serializer.data}
                return Response(context, status.HTTP_200_OK)
            else:
                message = 'Account deactivated'
                context = {'success': False, 'message': message, 'error': ''}
                return Response(context, status.HTTP_400_BAD_REQUEST)

        else:
            message = 'Invalid Login Creds'
            context = {'success': False, 'message': message, 'error': ''}
            return Response(context, status.HTTP_400_BAD_REQUEST)


