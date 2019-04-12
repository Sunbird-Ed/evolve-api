from django.shortcuts import render
from .models import OtherContributors
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from .serializers import OtherContributorSerializer

# Create your views here.
class OtherContributorCreateView(ListCreateAPIView):
    queryset = OtherContributors.objects.all()
    serializer_class = OtherContributorSerializer
    def post(self, request):      
        try:
            queryset = OtherContributors.objects.filter(first_name__iexact=request.data['first_name'].strip(),last_name__iexact=request.data['last_name'].strip(), mobile=request.data['mobile'].strip(), tag__id=request.data['tag']).first()
            if queryset is not None:
                if str(queryset.email) == "" and request.data['email'] is not None:
                    ContentContributors.objects.filter(id=queryset.id).update(email=request.data['email'])
                    queryset.refresh_from_db()
                serializer = OtherContributorSerializer(queryset)
                context = {"success": True, "message": "Successful",  "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer = OtherContributorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    context = {"success": True, "message": "Successful",  "data": serializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                context = {"success": False, "message": "Invalid Input Data to create Pesonal details"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to Personal Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)