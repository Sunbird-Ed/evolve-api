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
from .serializers import (
    ContentListSerializer,
    BookNestedSerializer,
    BookListSerializer, 
    ContentStatusListSerializer,
    SectionKeywordSerializer,
    SubSectionKeywordSerializer,
    SectionKeywordsSerializer,
    ChapterKeywordsSerializer,
    SubSectionKeywordsSerializer,
    KeywordSerializer,
    ContentContributorSerializer,
    ApprovedContentSerializer,
    ContentStatusSerializer,
    HardSpotCreateSerializer, 
    ContentContributorsSerializer,
    SubSubSectionKeywordsSerializer,)

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.parsers import MultiPartParser
from apps.dataupload.models import (Chapter,
    Section,
    SubSection,
    ChapterKeyword,
    SectionKeyword,
    SubSectionKeyword,
    SubSubSectionKeyword,
    )
import json
import pandas as pd
from evolve import settings

from evolve import settings
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions
)
from datetime import datetime, timedelta
import os
import itertools
from django.db.models import Q

account_name = settings.AZURE_ACCOUNT_NAME
account_key = settings.AZURE_ACCOUNT_KEY
CONTAINER_NAME= settings.AZURE_CONTAINER


block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)


class ContentList(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = ContentStatusListSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Chapter list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,format=None):
        try:
         
            serializer = ContentListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Created Successful", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Invalid Input Data to create content"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to create content.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class ContentRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer

    def get(self, request):
        try:
            queryset = self.get_object()
            serializer = ContentListSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get content list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            try:
                content_list = self.get_object()

            except Exception as error:
                context = {'success': "false", 'message': 'content Id does not exist.'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            serializer = ContentListSerializer(content_list, data=request.data, context={"user":request.user}, partial=True)

            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Updation Successful","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Updation Failed"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed To Update content Details.'}
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
                context = {"success": True, "message": "Conetent List","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Content list.'}
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
                context = {"success": True, "message": "Content List","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Conetent list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentApprovedList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=True)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=True)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=True)
            elif  sub_sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=True)
            else:
                queryset = self.get_queryset().filter(approved=True)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Approved List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content Approved list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ContentPendingList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = KeywordSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)

            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False, approved_by=None)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=False, approved_by=None)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False, approved_by=None)
            elif sub_sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=False,approved_by=None)
            else:
                queryset = self.get_queryset().filter(approved=False, approved_by=None)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Pending List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content Pending list.'}
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
            context = {"success": True, "message": "Content Status List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content Status list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentRejectedList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False).exclude(approved_by=None)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id, approved=False).exclude(approved_by=None)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False).exclude(approved_by=None)
            elif sub_sub_section_id is not None:
                queryset =self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id , approved = False).exclude(approved_by=None)
            else:
                queryset = self.get_queryset().filter(approved=False).exclude(approved_by=None)
            serializer = KeywordSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Rejected List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content Rejected list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Keywords(ListAPIView):
    queryset = Content.objects.all()

    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section', None)
            if chapter_id is not None:
                queryset=ChapterKeyword.objects.filter(chapter__id = chapter_id)
                serializer = ChapterKeywordsSerializer(queryset, many=True)
            elif section_id is not None:
                queryset = SectionKeyword.objects.filter(section__id = section_id)
                serializer = SectionKeywordsSerializer(queryset, many=True)
            elif sub_section_id is not None:
                queryset = SubSectionKeyword.objects.filter(sub_section__id = sub_section_id)
                serializer = SubSectionKeywordsSerializer(queryset, many=True)
            elif sub_sub_section_id is not None:
                queryset = SubSubSectionKeyword.objects.filter(sub_sub_section__id = sub_sub_section_id)
                serializer = SubSubSectionKeywordsSerializer(queryset, many=True)
            else:   
                queryset = self.get_queryset()
                serializer = KeywordSerializer(queryset, many=True)

            context = {"success": True, "message": "Content List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content list.'}
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
                context = {"success": True, "message": "Successful",  "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer = ContentContributorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    context = {"success": True, "message": "Successful",  "data": serializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                context = {"success": False, "message": "Invalid Input Data to create Pesonal details"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to Personal Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

@permission_classes((IsAuthenticated,))
class ApprovedContentDownloadView(ListAPIView):
    queryset = Book.objects.all()

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            book = request.query_params.get('book', None)
            chapters=Chapter.objects.filter(book_id=book).order_by('id')
            serializer = ApprovedContentSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            repeat_list=['Content Name','Content Link/Video Link','Content Rating (By Reviewer)','Comment (By Reviewer)', 'linked_keywords']

            data_frame = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords',]+(list(itertools.chain.from_iterable(itertools.repeat(repeat_list, 5)))))
            exists = os.path.isfile('ApprovedContent.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('ApprovedContent.csv')
            data_frame.to_csv(path + 'ApprovedContent.csv', encoding="utf-8-sig", index=False)
     
            context = {"success": True, "message": "Activity List",  "data": 'media/files/ApprovedContent.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentStatusDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            book_id = request.query_params.get('book', None)
            book_name=""
            if book_id is not None:
                book_name=Book.objects.get(id=book_id)
                chapters=Chapter.objects.filter(book__id=book_id).order_by('id')
            serializer = ContentStatusSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['Board', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'total', 'approved_contents', 'rejected_contents', 'pending_contents', 'hard_spots'])
            exists = os.path.isfile('{}_contentstatus.csv'.format(book_name))
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('{}_contentstatus.csv'.format(book_name))
            # data_frame.to_excel(path + 'contentstatus.xlsx')
            data_frame.to_csv(path + str(book_name)+'_contentstatus.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List","data": 'media/files/{}_contentstatus.csv'.format(book_name)}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class ContentContributorsDownloadView(RetrieveUpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            state_id = request.query_params.get('state', None)
            if state_id is not None:
                queryset = Content.objects.filter(Q(sub_sub_section__subsection__section__chapter__book__subject__grade__medium__state__id=state_id) | Q(sub_section__section__chapter__book__subject__grade__medium__state__id = state_id) | Q(section__chapter__book__subject__grade__medium__state__id= state_id) | Q(chapter__book__subject__grade__medium__state__id = state_id) ).distinct()
            else:
                queryset = self.get_queryset()
            serializer = ContentContributorsSerializer(queryset, many=True)
            res_list = [] 
            for i in range(len(serializer.data)): 
                if serializer.data[i] not in serializer.data[i + 1:]: 
                    res_list.append(serializer.data[i])
            for data in res_list:
                for d in res_list:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email','city_name','school_name','textbook_name']).drop_duplicates()
            exists = os.path.isfile('content_contributers.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('content_contributers.csv')
            # data_frame.to_excel(path + 'content_contributers.xlsx')
            data_frame.to_csv(path + 'content_contributers.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List","data": 'media/files/content_contributers.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = { 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetSASView(ListAPIView):

    def get(self,request):
        try:
            sas_url = block_blob_service.generate_container_shared_access_signature(
                CONTAINER_NAME,
                ContainerPermissions.WRITE,
                datetime.utcnow() + timedelta(hours=1),
            )
            base_url=account_name+".blob.core.windows.net/"+CONTAINER_NAME
            context = {"success": True, "message": "url link", "token":sas_url,"base_url":base_url}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSasDownloadView(ListAPIView):
    
    def get(self,request):
        from evolve import settings
        accountName = settings.AZURE_ACCOUNT_NAME
        accountKey = settings.AZURE_ACCOUNT_KEY
        containerName= settings.AZURE_CONTAINER
        try:
            blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
            sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=10))
            context = {"success": True, "token":sas_token}
            return Response(context, status=status.HTTP_200_OK)
        except:
            return None



            
      
