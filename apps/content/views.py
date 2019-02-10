from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from apps.configuration.models import Book
from apps.hardspot.models import  HardSpot
from .models import Content,ContentContributors
from .serializers import ContentListSerializer,BookNestedSerializer,BookListSerializer, ContentStatusListSerializer,SectionKeywordSerializer,SubSectionKeywordSerializer,SectionKeywordsSerializer,ChapterKeywordsSerializer,SubSectionKeywordsSerializer,KeywordSerializer,ContentContributorSerializer,ApprovedContentSerializer,ContentStatusSerializer,HardSpotCreateSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.parsers import MultiPartParser
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword
import json
import pandas as pd
from evolve import settings

class ContentList(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = ContentStatusListSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Chapter list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,format=None):
        try:
         
            serializer = ContentListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Created Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Invalid Input Data to create content", "error": str(serializer.errors)}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to create content.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class ContentRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer

    def get(self, request):
        try:
            queryset = self.get_object()
            serializer = ContentListSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get content list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            try:
                # 
                content_list = self.get_object()

            except Exception as error:
                context = {'error': "content Id does not exist", 'success': "false", 'message': 'content Id does not exist.'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            serializer = ContentListSerializer(content_list, data=request.data, context={"user":request.user}, partial=True)

            if serializer.is_valid():
                # import ipdb;ipdb.set_trace()
                serializer.save()
                context = {"success": True, "message": "Updation Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Updation Failed", "error": str(serializer.errors)}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed To Update content Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class BookNestedList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookNestedSerializer

    def get(self, request):
            try:
                subject = request.query_params.get('subject', None)
                if subject is not None:
                    queryset=self.get_queryset().filter(subject__id=subject, content_only=True)
                else:
                    queryset = self.get_queryset().filter(content_only=True)
                serializer = BookNestedSerializer(queryset, many=True)
                context = {"success": True, "message": "Conetent List", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def get(self, request):
            try:
                subject = request.query_params.get('subject', None)
                if subject is not None:
                    queryset=self.get_queryset().filter(subject__id=subject)
                else:
                    queryset = self.get_queryset()
                serializer = BookListSerializer(queryset, many=True)
                context = {"success": True, "message": "Content List", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'error': str(error), 'success': "false", 'message': 'Failed to get Conetent list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentApprovedList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            # import pdb; pdb.set_trace()
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=True)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=True)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=True)
            else:
                queryset = self.get_queryset().filter(approved=True)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Approved List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content Approved list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ContentPendingList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            # import pdb; pdb.set_trace()
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False, approved_by=None)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=False, approved_by=None)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False, approved_by=None)
            else:
                queryset = self.get_queryset().filter(approved=False, approved_by=None)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Pending List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content Pending list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ContentStatusList(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer


    def get(self, request):
        try:
    
            if request.query_params.get('chapter', None) is not None:
                queryset=self.get_queryset().filter(chapter_id=request.query_params.get('chapter', None))
            elif request.query_params.get('section', None) is not None:
                queryset=self.get_queryset().filter(chapter_id=request.query_params.get('section', None))
            elif request.query_params.get('section', None) is not None:
                queryset=self.get_queryset().filter(chapter_id=request.query_params.get('sub_section', None))       
            else:
                queryset = self.get_queryset()
            serializer = ContentListSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Status List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content Status list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentRejectedList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            # import pdb; pdb.set_trace()
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False).exclude(approved_by=None)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=False).exclude(approved_by=None)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False).exclude(approved_by=None)
            else:
                queryset = self.get_queryset().filter(approved=False).exclude(approved_by=None)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Rejected List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content Rejected list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Keywords(ListAPIView):
    queryset = Content.objects.all()

    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            if chapter_id is not None:
                queryset=ChapterKeyword.objects.filter(chapter__id = chapter_id)
                serializer = ChapterKeywordsSerializer(queryset, many=True)
            elif section_id is not None:
                queryset = SectionKeyword.objects.filter(section__id = section_id)
                serializer = SectionKeywordsSerializer(queryset, many=True)
            elif sub_section_id is not None:
                queryset = SubSectionKeyword.objects.filter(sub_section__id = sub_section_id)
                serializer = SubSectionKeywordsSerializer(queryset, many=True)
            else:   
                queryset = self.get_queryset()
                serializer = KeywordSerializer(queryset, many=True)

            context = {"success": True, "message": "Content List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Content list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ContentContributorCreateView(ListCreateAPIView):
    queryset = ContentContributors.objects.all()
    serializer_class = ContentContributorSerializer
    def post(self, request):      
        try:
            queryset = ContentContributors.objects.filter(first_name__iexact=request.data['first_name'].strip(),last_name__iexact=request.data['last_name'].strip(), mobile=request.data['mobile'].strip()).first()
            if queryset is not None:
                if str(queryset.email) == "" and request.data['email'] is not None:
                    ContentContributors.objects.filter(id=queryset.id).update(email=request.data['email'])
                    queryset.refresh_from_db()
                serializer = ContentContributorSerializer(queryset)
                context = {"success": True, "message": "Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer = ContentContributorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    context = {"success": True, "message": "Successful", "error": "", "data": serializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                context = {"success": False, "message": "Invalid Input Data to create Pesonal details", "error": str(serializer.errors)}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to Personal Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  


class ApprovedContentDownloadView(ListAPIView):
    queryset = Book.objects.all()

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            book = request.query_params.get('book', None)
            # chapters=Chapter.objects.all()
            chapters=Chapter.objects.filter(book_id=book)
            serializer = ApprovedContentSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    if len(d) == 13:
                        final_list.append(d)
                    elif len(d) == 11:
                        d.append(" ")
                        d.append(" ")
                        final_list.append(d)
                    elif len(d) == 12:
                        d.append(" ")
                        final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['State', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'Keywords','content_name','video','rating','comment'])
            exists = os.path.isfile('ApprovedContent.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('ApprovedContent.csv')
            data_frame.to_csv(path + 'ApprovedContent.csv', encoding="utf-8-sig", index=False)
     
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/ApprovedContent.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentStatusDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            # import ipdb; ipdb.set_trace()
            final_list = []
            import os
            from shutil import copyfile
            book_id = request.query_params.get('book', None)
            if book_id is not None:
                chapters=Chapter.objects.filter(book__id=book_id)
            serializer = ContentStatusSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['State', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'total', 'approved_contents', 'rejected_contents', 'pending_contents', 'hard_spots'])
            exists = os.path.isfile('contentstatus.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('contentstatus.xlsx')
            data_frame.to_excel(path + 'contentstatus.xlsx')
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/contentstatus.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
