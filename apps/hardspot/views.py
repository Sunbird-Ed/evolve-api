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
from .serializers import HardSpotCreateSerializer,BookNestedSerializer, HardSpotUpdateSerializer, HardspotVisitersSerializer, ContentVisitersSerializer,HardSpotContributorSerializer,ApprovedHardSpotSerializer,HardspotStatusSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
import pandas as pd
from evolve import settings



class HardSpotListOrCreateView(ListCreateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
    def post(self, request):      
        try:
            serializer = HardSpotCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Thank you for the submission.\nWe will review and get back to you", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Invalid Input Data to create Pesonal details", "error": str(serializer.errors)}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to Personal Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            if chapter_id is not None:
                queryset=self.get_queryset().filter(chapter__id=chapter_id)
            elif section_id is not None:
                queryset = self.get_queryset().filter(section__id=section_id)
            elif sub_section_id is not None:
                queryset = self.get_queryset().filter(sub_section__id=sub_section_id)
            else:
                queryset = self.get_queryset()
                serializer = HardSpotSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HardSpotApprovedList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
  
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
                queryset = self.get_queryset()
            serializer = HardSpotCreateSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HardSpotPendingList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
  
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
                queryset = self.get_queryset()
            serializer = HardSpotCreateSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HardSpotStatusList(ListCreateAPIView):

    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer


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
            serializer = HardSpotCreateSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HardSpotRejectedList(ListAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
  
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
                queryset = self.get_queryset()
            serializer = HardSpotCreateSerializer(queryset, many=True)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
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
                context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class HardSpotUpdateView(RetrieveUpdateAPIView):
    queryset = HardSpot.objects.all()
    serializer_class = HardSpotCreateSerializer
  
    def get(self, request,pk):
        try:
            queryset = self.get_object()
            serializer = HardSpotSerializer(queryset)
            context = {"success": True, "message": "HardSpot List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get HardSpot list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            try:
                hardspot_detail = self.get_object()

            except Exception as error:
                context = {'error': "Hardsport Id does not exist", 'success': "false", 'message': 'Hardsport Id does not exist.'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            if request.data['approved']:
                serializer = HardSpotUpdateSerializer(hardspot_detail, data=request.data, context={"user":request.user}, partial=True)
            else:
                serializer = HardSpotUpdateSerializer(hardspot_detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Updation Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Updation Failed", "error": str(serializer.errors)}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed To Update Hardsport Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HardspotContributorDownloadView(RetrieveUpdateAPIView):
    queryset = HardSpotContributors.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            # import ipdb; ipdb.set_trace()
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
                # for key, value in data.items():
                #     final_list.append(value)

            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email']).drop_duplicates()
            exists = os.path.isfile('hardspot_contributers.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('hardspot_contributers.xlsx')
            data_frame.to_excel(path + 'hardspot_contributers.xlsx')
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/hardspot_contributers.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentContributorDownloadView(RetrieveUpdateAPIView):
    queryset = ContentContributors.objects.all()
    serializer_class = HardSpotCreateSerializer

    def get(self, request):
        try:
            # import ipdb; ipdb.set_trace()
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
                # for key, value in data.items():
                #     final_list.append(value)

            data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email']).drop_duplicates()
            exists = os.path.isfile('content_contributers.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('content_contributers.xlsx')
            data_frame.to_excel(path + 'content_contributers.xlsx')
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/content_contributers.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
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
                context = {"success": True, "message": "Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                serializer = HardSpotContributorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    context = {"success": True, "message": "Successful", "error": "", "data": serializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                context = {"success": False, "message": "Invalid Input Data to create Pesonal details", "error": str(serializer.errors)}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to Personal Details.'}
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
                chapters=Chapter.objects.filter(book_id=book)
                serializer = ApprovedHardSpotSerializer(chapters, many=True)
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

                data_frame = pd.DataFrame(final_list , columns=['State', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'Keywords','hard_spot','description','points_to_be_covered','useful_to'])
                exists = os.path.isfile('ApprovedHardSpot.csv')
                path = settings.MEDIA_ROOT + '/files/'
                if exists:
                    os.remove('ApprovedHardSpot.csv')
                data_frame.to_csv(path + 'ApprovedHardSpot.csv', encoding="utf-8-sig", index=False)
        
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/ApprovedHardSpot.csv'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HardSpotStatusDownloadView(RetrieveUpdateAPIView):
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
            serializer = HardspotStatusSerializer(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['State', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'total', 'approved_Hardspot', 'rejected_hardspot', 'pending_hardspot'])
            exists = os.path.isfile('hardspotstatus.xlsx')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('hardspotstatus.xlsx')
            data_frame.to_excel(path + 'hardspotstatus.xlsx')
            context = {"success": True, "message": "Activity List", "error": "", "data": 'media/files/hardspotstatus.xlsx'}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Activity list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
