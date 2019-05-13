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
from apps.dataupload.models import Chapter,Section,SubSection
from .models import HardSpot,HardSpotContributors
from apps.content.models import Content, ContentContributors
from .serializers import HardSpotCreateSerializer, BookNestedSerializer, HardSpotUpdateSerializer, HardspotVisitersSerializer, ContentVisitersSerializer,HardSpotContributorSerializer,ApprovedHardSpotSerializer,HardspotStatusSerializer, HardspotContributorsSerializer, HardSpotSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
import pandas as pd
from evolve import settings
from django.db.models import Q
class HardSpotListOrCreateView(ListCreateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
    def post(self, request):      
        try:
            serializer = HardSpotCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Thank you for the submission.\nWe will review and get back to you", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Invalid Input Data to create Pesonal details",}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to Personal Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section', None)
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id,approved=True)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id,approved=True)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id,approved=True)
            elif sub_sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_sub_section__id=sub_sub_section_id,approved=True)
            else:
                queryset = self.get_queryset()
            serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HardSpotApprovedList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotSerializer
  
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
            elif sub_sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_sub_section__id=sub_sub_section_id, approved=True)
            else:
                queryset = self.get_queryset()
            serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HardSpotPendingList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotSerializer
  
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
                queryset = self.get_queryset().filter(sub_sub_section__id=sub_sub_section_id, approved=False, approved_by=None)
            else:
                queryset = self.get_queryset()
            serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HardSpotStatusList(ListCreateAPIView):

    queryset = HardSpot.objects.all()
    serializer_class = HardSpotSerializer


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
            serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HardSpotRejectedList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotSerializer
  
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
                queryset = self.get_queryset().filter(sub_sub_section__id=sub_sub_section_id, approved=False).exclude(approved_by=None)
            else:
                queryset = self.get_queryset()
            serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List",  "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookNestedList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookNestedSerializer

    def get(self, request):
            try:
                subject = request.query_params.get('subject', None)
                if subject is not None:
                    queryset=self.get_queryset().filter(subject__id=subject, hardspot_only=True)
                else:
                    queryset = self.get_queryset().filter(hardspot_only=True)
                serializer = BookNestedSerializer(queryset, many=True)
                context = {"success": True, "message": "HardSpot List",  "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class HardSpotUpdateView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotSerializer
  
    def get(self, request,pk):
        try:
            queryset = self.get_object()
            serializer = HardSpotSerializer(queryset)
            context = {"success": True, "message": "HardSpot List",  "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            try:
                hardspot_detail = self.get_object()

            except Exception as error:
                context = { 'success': "false", 'message': 'Hardsport Id does not exist.'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            if request.data['approved']:
                serializer = HardSpotUpdateSerializer(hardspot_detail, data=request.data, context={"user":request.user}, partial=True)
            else:
                serializer = HardSpotUpdateSerializer(hardspot_detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Updation Successful", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Updation Failed"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed To Update Hardsport Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HardspotVisitorsDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpotContributors.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            queryset = self.get_queryset()
            serializer = HardspotVisitersSerializer(queryset, many=True)
            res_list = [] 
            for i in range(len(serializer.data)): 
                if serializer.data[i] not in serializer.data[i + 1:]: 
                    res_list.append(serializer.data[i])
            for data in res_list:
                for d in res_list:
                    final_list.append(d)


            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email']).drop_duplicates()
            exists = os.path.isfile('hardspot_contributers.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('hardspot_contributers.xlsx')
            data_frame.to_csv(path + 'hardspot_contributers.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List", "data": 'media/files/hardspot_contributers.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentVisitorsDownloadView(RetrieveUpdateAPIView):
    queryset = ContentContributors.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            queryset = self.get_queryset()
            serializer = ContentVisitersSerializer(queryset, many=True)
            res_list = [] 
            for i in range(len(serializer.data)): 
                if serializer.data[i] not in serializer.data[i + 1:]: 
                    res_list.append(serializer.data[i])
            for data in res_list:
                for d in res_list:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email']).drop_duplicates()
            exists = os.path.isfile('content_contributers.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('content_contributers.xlsx')
            data_frame.to_csv(path + 'content_contributers.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List","data": 'media/files/content_contributers.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HardSpotContributorCreateView(ListCreateAPIView):
    queryset = HardSpotContributors.objects.all()
    serializer_class = HardSpotContributorSerializer
    def post(self, request):      
        try:
            queryset = HardSpotContributors.objects.filter(first_name__iexact=request.data['first_name'].strip(),last_name__iexact=request.data['last_name'].strip(), mobile=request.data['mobile'].strip()).first()
            if queryset is not None:
                if str(queryset.email) == "" and request.data['email'] is not None:
                    HardSpotContributors.objects.filter(id=queryset.id).update(email=request.data['email'])
                    queryset.refresh_from_db()
                serializer = HardSpotContributorSerializer(queryset)
                context = {"success": True, "message": "Successful", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer = HardSpotContributorSerializer(data=request.data)
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
class ApprovedHardSpotDownloadView(ListAPIView):
    queryset = Book.objects.all()

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            book = request.query_params.get('book', None)
            if book is not None:
                chapters=Chapter.objects.filter(book_id=book).order_by('id')
                serializer = ApprovedHardSpotSerializer(chapters, many=True)
                for data in serializer.data:
                    for d in data['chapter']:
                        final_list.append(d)
                
                data_frame = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords','What topic is difficult to understand in this section ?','Why is this a difficult topic?','In the video to be created for this hard spot, what points/aspects do you want to be covered and addressed ?','Who do you think needs additional digital content for this hard spot?','Hardspot Rating (By Reviewer)','Comment (By Reviewer)','What topic is difficult to understand in this section ?','Why is this a difficult topic?','In the video to be created for this hard spot, what points/aspects do you want to be covered and addressed ?','Who do you think needs additional digital content for this hard spot?','Hardspot Rating (By Reviewer)','Comment (By Reviewer)','What topic is difficult to understand in this section ?','Why is this a difficult topic?','In the video to be created for this hard spot, what points/aspects do you want to be covered and addressed ?','Who do you think needs additional digital content for this hard spot?','Hardspot Rating (By Reviewer)','Comment (By Reviewer)','What topic is difficult to understand in this section ?','Why is this a difficult topic?','In the video to be created for this hard spot, what points/aspects do you want to be covered and addressed ?','Who do you think needs additional digital content for this hard spot?','Hardspot Rating (By Reviewer)','Comment (By Reviewer)','What topic is difficult to understand in this section ?','Why is this a difficult topic?','In the video to be created for this hard spot, what points/aspects do you want to be covered and addressed ?','Who do you think needs additional digital content for this hard spot?','Hardspot Rating (By Reviewer)','Comment (By Reviewer)'])
                exists = os.path.isfile('ApprovedHardSpot.csv')
                path = settings.MEDIA_ROOT + '/files/'
                if exists:
                    os.remove('ApprovedHardSpot.csv')
                data_frame.to_csv(path + 'ApprovedHardSpot.csv', encoding="utf-8-sig", index=False)
        
            context = {"success": True, "message": "Activity List", "data": 'media/files/ApprovedHardSpot.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HardSpotStatusDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            final_list = []
            import os
            from shutil import copyfile
            book_id = request.query_params.get('book', None)
            if book_id is not None:
                chapters=Chapter.objects.filter(book__id=book_id).order_by("id")
            serializer = HardspotStatusSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['Board', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'total', 'approved_Hardspot', 'rejected_hardspot', 'pending_hardspot'])
            exists = os.path.isfile('hardspotstatus.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('hardspotstatus.csv')
            data_frame.to_csv(path + 'hardspotstatus.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List",  "data": 'media/files/hardspotstatus.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = { 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes((IsAuthenticated,))
class HardspotContributorsDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            state_id = request.query_params.get('state', None)
            final_list = []
            import os
            from shutil import copyfile
            if state_id is not None:
                queryset = HardSpot.objects.filter(Q(sub_sub_section__subsection__section__chapter__book__subject__grade__medium__state__id=state_id) | Q(sub_section__section__chapter__book__subject__grade__medium__state__id = state_id) | Q(section__chapter__book__subject__grade__medium__state__id= state_id) | Q(chapter__book__subject__grade__medium__state__id = state_id) ).distinct()
            else:
                queryset = self.get_queryset()
            serializer = HardspotContributorsSerializer(queryset, many=True)
            res_list = [] 
            for i in range(len(serializer.data)): 
                if serializer.data[i] not in serializer.data[i + 1:]: 
                    res_list.append(serializer.data[i])
            for data in res_list:
                for d in res_list:
                    final_list.append(d)


            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email','city_name','school_name','textbook_name']).drop_duplicates()
            exists = os.path.isfile('hard_spot_contributers.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('hard_spot_contributers.csv')
            data_frame.to_csv(path + 'hard_spot_contributers.csv', encoding="utf-8-sig", index=False)
            context = {"success": True, "message": "Activity List",  "data": 'media/files/hard_spot_contributers.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











