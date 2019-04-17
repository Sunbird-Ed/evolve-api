from django.shortcuts import render
from .models import OtherContributors
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import OtherContributorSerializer, OtherContentListSerializer,BookNestedSerializer
from .models import OtherContent, OtherContributors
from apps.configuration.models import Book
# Create your views here.
class OtherContributorCreateView(ListCreateAPIView):
    queryset = OtherContributors.objects.all()
    serializer_class = OtherContributorSerializer
    def post(self, request):      
        try:
            queryset = OtherContributors.objects.filter(first_name__iexact=request.data['first_name'].strip(),last_name__iexact=request.data['last_name'].strip(), mobile=request.data['mobile'].strip(), tags__id=request.data['tags']).first()
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

class OtherContentList(ListCreateAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentListSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = OtherContentListSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Chapter list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,format=None):
        try:
            serializer = OtherContentListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Created Successful", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Invalid Input Data to create content"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to create content.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class BookNestedList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookNestedSerializer

    def get(self, request):
            try:
                subject = request.query_params.get('subject', None)
                tag = request.query_params.get('tag', None)
                if subject is not None :
                    queryset=self.get_queryset().filter(subject__id=subject, content_only=True)
                else:
                    queryset = self.get_queryset().filter(content_only=True)
                if tag is not None:
                    serializer = BookNestedSerializer(queryset, many=True, context = {"tagname" : tag})
                context = {"success": True, "message": "Conetent List","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Content list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)