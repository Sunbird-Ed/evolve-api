from django.shortcuts import render
from .models import OtherContributors,Job
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser
from .serializers import (OtherContributorSerializer, 
    OtherContentListSerializer,
    BookNestedSerializer,
    SchoolNameSerializer,
    OtherContentBookListSerializer,
    OtherContentStatusSerializer,
    OtherContentStatusSerializer,
    OtherContentDetailListSerializer,
    OtherContentContributorsSerializer,
    ApprovedOtherContentSerializer,
    HardSpotDetailListSerializer,
    ContentDetailListSerializer,
    OtherContentStatusSerializerdownload,
    ApprovedOtherContentSerializerSecond,
    JobSerializer,
    )
from .models import OtherContent, OtherContributors,SchoolName,Tags
from apps.configuration.models import Book,State
from django.db.models import Q
import pandas as pd
from evolve import settings
import os
import re,string,random
from shutil import copyfile
import itertools
from apps.dataupload.models import Chapter
from apps.content.serializers import ApprovedContentSerializer,ContentContributorsSerializer,ApprovedOtherContentSerializerBulkDownload
from apps.hardspot.serializers import HardspotContributorsSerializer
from apps.hardspot.models import HardSpot
from apps.content.models import Content
import threading
# Create your views here.
class OtherContributorCreateView(ListCreateAPIView):
    queryset = OtherContributors.objects.all()
    serializer_class = OtherContributorSerializer
    def post(self, request):      
        try:
            queryset = OtherContributors.objects.filter(first_name__iexact=request.data['first_name'].strip(),last_name__iexact=request.data['last_name'].strip(), mobile=request.data['mobile'].strip(), tags__id=request.data['tags']).first()
            if queryset is not None:
                if str(queryset.email) == "" and request.data['email'] is not None:
                    OtherContributors.objects.filter(id=queryset.id).update(email=request.data['email'])
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
            context = {'success': "false", 'message': 'Failed to create content.', "error": str(error)}
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
                context = {"success": True, "message": "Content List","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Content list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class SchoolNameList(ListAPIView):
    queryset = SchoolName.objects.all()
    serializer_class = SchoolNameSerializer

    def get(self, request):
            try:
                queryset = self.get_queryset().order_by('school_name')
                serializer = SchoolNameSerializer(queryset, many=True)
                sorted_data=(sorted(serializer.data, key = lambda i: re.sub('[^A-Za-z]+', '', str(i['school_name']).strip())))

                context = {"success": True, "message": "Schools List","data": sorted_data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Schools list.'}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class OtherBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = OtherContentBookListSerializer

    def get(self, request):
            try:
                subject = request.query_params.get('subject', None)
                tag = request.query_params.get('tag',None)
                school_name = request.query_params.get('school',None)
                if school_name is None:
                    school_name = "0"
                if subject is not None:
                    queryset=self.get_queryset().filter(subject__id=subject)
                elif subject is None or school_name == "0":
                    queryset = self.get_queryset()
                if tag is not None:
                    serializer = OtherContentBookListSerializer(queryset, many=True ,context={'tag_code': tag,'school_name':school_name})
                 
                context = {"success": True, "message": "Content List","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            except Exception as error:
                context = {'success': "false", 'message': 'Failed to get Conetent list.',"error":error}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class UpdateOtherContentView(RetrieveUpdateAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContributorSerializer
    
    def put(self, request, pk, format=None):
        try:
            try:
                content_list = self.get_object()

            except Exception as error:
                context = {'success': "false", 'message': 'othercontent Id does not exist.'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            serializer = OtherContentStatusSerializer(content_list, data=request.data, context={"user":request.user}, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Updation Successful","data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            context = {"success": False, "message": "Updation Failed"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed To Update othercontent Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class OtherContentApprovedList(ListAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentStatusSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)
            tag = request .query_params.get('tag',None)
            school_name = request.query_params.get('school', None)
            if school_name == "null":
                school_name = "0"
            if school_name is None or school_name == "0":
                if chapter_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(chapter__id=chapter_id, approved=True,tags__id=tag)
                elif section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=True,tags__id=tag)
                elif sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=True,tags__id=tag)
                elif  sub_sub_section_id is not None and tag is not None: 
                    queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=True,tags__id=tag)
                else:
                    queryset = self.get_queryset().filter(approved=True,tags__id=tag)
            elif school_name is not None and school_name != "0":
                if chapter_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(chapter__id=chapter_id, approved=True,tags__id=tag,content_contributors__school_name__id=school_name)
                elif section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=True,tags__id=tag,content_contributors__school_name__id=school_name)
                elif sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=True,tags__id=tag,content_contributors__school_name__id=school_name)
                elif  sub_sub_section_id is not None and tag is not None: 
                    queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=True,tags__id=tag,content_contributors__school_name__id=school_name)
                else:
                    queryset = self.get_queryset().filter(approved=True,tags__id=tag)

            serializer = OtherContentStatusSerializer(queryset, many=True)
            context = {"success": True, "message": "OtherContent Approved List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get OtherContent Approved list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   





class OtherContentPendingList(ListAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentStatusSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)
            tag = request.query_params.get('tag',None)
            school_name = request.query_params.get('school', None)
            if school_name == "null":
                school_name = "0"
            if school_name is None or school_name == "0":
                if chapter_id is not None and tag is not None:
                    queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False, approved_by=None,tags__id=tag)
                elif section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=False, approved_by=None,tags__id=tag)
                elif sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False, approved_by=None,tags__id=tag)
                elif sub_sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=False,approved_by=None,tags__id=tag)
                else:
                    queryset = self.get_queryset().filter(approved=False, approved_by=None,tags__id=tag)

            elif school_name is not None and  school_name != "0":
                if chapter_id is not None and tag is not None:
                    queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False, approved_by=None,tags__id=tag,content_contributors__school_name__id=school_name)
                elif section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=False, approved_by=None,tags__id=tag,content_contributors__school_name__id=school_name)
                elif sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False, approved_by=None,tags__id=tag,content_contributors__school_name__id=school_name)
                elif sub_sub_section_id is not None and tag is not None:
                    queryset = self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id,approved=False,approved_by=None,tags__id=tag,content_contributors__school_name__id=school_name)
                else:
                    queryset = self.get_queryset().filter(approved=False, approved_by=None,tags__id=tag)

            serializer = OtherContentStatusSerializer(queryset, many=True)
            context = {"success": True, "message": "OtherContent Pending List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get OtherContent Pending list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OtherContentRejectedList(ListAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentStatusSerializer
  
    def get(self, request):
        try:
            chapter_id = request.query_params.get('chapter', None)
            section_id = request.query_params.get('section', None)
            sub_section_id = request.query_params.get('sub_section', None)
            sub_sub_section_id = request.query_params.get('sub_sub_section',None)
            tag = request.query_params.get('tag',None)
            school_name = request.query_params.get("school",None)
            if school_name == "null":
                school_name = "0"
            if school_name is None or school_name == "0":
                if chapter_id is not None:
                    queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False,tags__id=tag).exclude(approved_by=None)
                elif section_id is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=False,tags__id=tag).exclude(approved_by=None)
                elif sub_section_id is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False,tags__id=tag).exclude(approved_by=None)
                elif sub_sub_section_id is not None:
                    queryset =self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id , approved = False,tags__id=tag).exclude(approved_by=None)
                else:
                    queryset = self.get_queryset().filter(approved=False).exclude(approved_by=None,tags__id=tag)

            elif school_name is not None and school_name != "0":
                if chapter_id is not None:
                    queryset=self.get_queryset().filter(chapter__id=chapter_id, approved=False,tags__id=tag,content_contributors__school_name__id=school_name).exclude(approved_by=None)
                elif section_id is not None:
                    queryset = self.get_queryset().filter(section__id=section_id, approved=False,tags__id=tag,content_contributors__school_name__id=school_name).exclude(approved_by=None)
                elif sub_section_id is not None:
                    queryset = self.get_queryset().filter(sub_section__id=sub_section_id, approved=False,tags__id=tag,content_contributors__school_name__id=school_name).exclude(approved_by=None)
                elif sub_sub_section_id is not None:
                    queryset =self.get_queryset().filter(sub_sub_section__id = sub_sub_section_id , approved = False,tags__id=tag,content_contributors__school_name__id=school_name).exclude(approved_by=None)
                else:
                    queryset = self.get_queryset().filter(approved=False).exclude(approved_by=None,tags__id=tag)
            serializer = OtherContentStatusSerializer(queryset, many=True)
            context = {"success": True, "message": "Content Rejected List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Content Rejected list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @permission_classes((IsAuthenticated,))
class OtherContentDetailList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = OtherContentDetailListSerializer
    def get(self, request):
        try:
            state = request.query_params.get('state', None)
            tag = request.query_params.get('tag',None)
            if state is not None and tag is not None:
                queryset=self.get_queryset().filter(subject__grade__medium__state_id=state,)
                if tag == "1":
                    serializer = ContentDetailListSerializer(queryset, many=True)
                elif tag == "2": 
                    serializer = HardSpotDetailListSerializer(queryset, many=True)
                else:
                    serializer = OtherContentDetailListSerializer(queryset, many=True, context={'code_name': tag})
            else:
                queryset = self.get_queryset()
                serializer = OtherContentDetailListSerializer   (queryset, many=True)
            context = {"success": True, "message": "List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes((IsAuthenticated,))
class OtherContentContributorsDownloadView(RetrieveUpdateAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentContributorsSerializer

    

    def get(self ,request):
        try:
            state_id = request.query_params.get('state', None)
            tag = request.query_params.get('tag',None)
            # tag interchage
            
            if tag is not None and state_id is not None:
                tag_name = str(Tags.objects.get(id=tag).tag_name)
                state_name=State.objects.get(id=state_id).state
            random_str = ''.join(random.choice(string.ascii_letters) for m in range(4))
            if Job.objects.filter(task_id=random_str).exists() is False:
                data = Job(task_id=random_str, status=False)
                data.save()
            else:
                exists.status = False
                exists.save()
            t = threading.Thread(target=self.index, args=(request,state_id,state_name,tag,tag_name,random_str), kwargs={})
            t.setDaemon(True)
            t.start()
            context = {"success": True, "message": "Activity List","data": 'media/files/{}_{}_contributers.csv'.format(str(state_name),tag_name),"id":random_str}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = { 'success': "false", 'message': 'Failed to get Activity list.',"error":  str(error)}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def index(self, request,state_id,state_name,tag,tag_name,random_str):
        try:
            final_list = []
            if state_id is not None and tag == "1":
                queryset = Content.objects.filter(Q(sub_sub_section__subsection__section__chapter__book__subject__grade__medium__state__id=state_id) | Q(sub_section__section__chapter__book__subject__grade__medium__state__id = state_id) | Q(section__chapter__book__subject__grade__medium__state__id= state_id) | Q(chapter__book__subject__grade__medium__state__id = state_id) ).distinct()
                serializer = ContentContributorsSerializer(queryset, many=True)
                res_list = [] 
                for i in range(len(serializer.data)): 
                    if serializer.data[i] not in serializer.data[i + 1:]: 
                        res_list.append(serializer.data[i])
                for data in res_list:
                    for d in res_list:
                        final_list.append(d)
                data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email','city_name','school_name','textbook_name','grade','subject']).drop_duplicates()
            elif tag == "2":
                queryset = HardSpot.objects.filter(Q(sub_sub_section__subsection__section__chapter__book__subject__grade__medium__state__id=state_id) | Q(sub_section__section__chapter__book__subject__grade__medium__state__id = state_id) | Q(section__chapter__book__subject__grade__medium__state__id= state_id) | Q(chapter__book__subject__grade__medium__state__id = state_id) ).distinct()
                serializer = HardspotContributorsSerializer(queryset, many=True)
                res_list = [] 
                for i in range(len(serializer.data)): 
                    if serializer.data[i] not in serializer.data[i + 1:]: 
                        res_list.append(serializer.data[i])
                for data in res_list:
                    for d in res_list:
                        final_list.append(d)
                data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email','city_name','school_name','textbook_name','grade','subject']).drop_duplicates()
            else:
                if tag is not None:
                    queryset = OtherContent.objects.filter(Q(sub_sub_section__subsection__section__chapter__book__subject__grade__medium__state__id=state_id,tags__id=tag)| Q(sub_section__section__chapter__book__subject__grade__medium__state__id = state_id,tags__id=tag)| Q(section__chapter__book__subject__grade__medium__state__id= state_id,tags__id=tag) | Q(chapter__book__subject__grade__medium__state__id = state_id , tags__id=tag) ).distinct()
                    serializer = OtherContentContributorsSerializer(queryset, many=True )
                res_list = [] 

                for i in range(len(serializer.data)): 
                    if serializer.data[i] not in serializer.data[i + 1:]: 
                        res_list.append(serializer.data[i])
                for data in res_list:
                    for d in res_list:
                        final_list.append(d)
                data_frame = pd.DataFrame(final_list , columns=['first_name', 'last_name','mobile', 'email','school_name','textbook_name','grade','subject']).drop_duplicates()
            path = settings.MEDIA_ROOT + '/files/'
            exists = os.path.isfile(path+str(state_name)+'_{}_contributers.csv'.format(tag_name))
            ff = ""
            if exists:
                os.remove(path+str(state_name)+'_{}_contributers.csv'.format(tag_name))
                if os.path.isfile(path+str(state_name)+'_{}_contributers.csv'.format(tag_name)):
                    ff = "file exist" 
                else:
                    ff = "file removed"
            data_frame.to_csv(path +str(state_name)+ '_{}_contributers.csv'.format(tag_name), encoding="utf-8-sig", index=False)
            t = Job.objects.get(task_id=random_str)
            t.status = True  # change field
            t.save()
        except Exception as error:
            print(str(error))
           


# @permission_classes((IsAuthenticated,))
class ApprovedOtherContentDownload(ListAPIView):
    queryset = Book.objects.all()

    def get(self, request):
        try:
            final_list = []
            state_id = request.query_params.get('state', None)
            book = request.query_params.get('book', None)
            tag = request.query_params.get('tag',None)
            status_ = request.query_params.get('status',None)
            chapters=Chapter.objects.filter(book_id=book).order_by('id')
            file_status= ""
            if tag == "1":
                serializer = ApprovedContentSerializer(chapters, many=True,context={"status" : str(status_)})

                for data in serializer.data:
                    for d in data['chapter']:
                        final_list.append(d)
                
                if str(status_) == "approved":
                    file_status = "Approved"
                    data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords','Content Name','Content Link',"Creators",'File format','linked_keywords'])
                if str(status_) == "rejected":

                    file_status = "Rejected"
                    data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords','Content Name','Content Link',"Creators",'File format','Comment','linked_keywords'])


            else:
                serializer = ApprovedOtherContentSerializer(chapters, many=True,context={'tag_id':tag, "status" : str(status_)})
                for data in serializer.data:
                    for d in data['chapter']:
                        final_list.append(d)
                
                if str(status_) == "approved":
                    file_status = "Approved"
                    data_frame1 = (pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Keywords','Content Name','Content Link/Video Link','text',"Creators",'Credit To','File format',"linked_keywords"]))
                if str(status_) == "rejected":
                    file_status = "Rejected"
                    data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Keywords','Content Name','Content Link/Video Link','text',"Creators",'Credit To','File format','Comment',"linked_keywords"])

                # repeat_list=['Content Name','Content Link/Video Link','text','linked_keywords']
                # data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords',]+(list(itertools.chain.from_iterable(itertools.repeat(repeat_list, 5)))))
            tag_name=""
            if tag == "10" or tag == "9":
                # video and pdf
                tag_name = Tags.objects.get(id=tag).tag_name
                data_frame=(data_frame1.drop(['text'], axis=1)).rename(index=str, columns={"Content Link/Video Link": "Content Link"})
                # data_frame=data_frame_.rename(index=str, columns={"Content Link/Video Link": "Content Document Link","Content Name":"Question"})
            elif tag == "8":
                # question answer
                tag_name = Tags.objects.get(id=tag).tag_name
                data_frame=(data_frame1.drop(['Content Link/Video Link'], axis=1)).rename(index=str, columns={"Content Name": "Question","text":"Answer"})

            elif tag == "7":
                # description
                tag_name = Tags.objects.get(id=tag).tag_name
                data_frame=(data_frame1.drop(['Content Link/Video Link','Content Name'], axis=1)).rename(index=str, columns={"text":"Learning Outcome Definition"})

            elif tag == "11":
                # only pdf
                tag_name = Tags.objects.get(id=tag).tag_name
                data_frame=(data_frame1.drop(['text'], axis=1)).rename(index=str, columns={"Content Link/Video Link":"Content Link"})
            else:
                data_frame=data_frame1
            state_name=State.objects.get(id=state_id).state
            exists = os.path.isfile(str(state_name)+"_"+str(tag_name)+'_'+file_status+'Content.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove(str(state_name)+"_"+str(tag_name)+'_'+file_status+'Content.csv')
            data_frame.to_csv(path + str(state_name) +"_"+str(tag_name)+'_'+file_status+'Content.csv', encoding="utf-8-sig", index=False)
     
            context = {"success": True, "message": "Activity List",  "data": 'media/files/{}_{}_{}Content.csv'.format(str(state_name),str(tag_name),str(file_status))}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.' ,"error" :error}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class OtherContentStatusDownloadView(RetrieveUpdateAPIView):
    queryset = OtherContent.objects.all()
    serializer_class = OtherContentStatusSerializer

    def get(self,request):
        try:
            book_id = request.query_params.get('book', None)
            state_id = request.query_params.get("state",None)
            if state_id is not None:
                t = threading.Thread(target=self.index, args=(request,book_id,state_id), kwargs={})
                t.setDaemon(True)
                t.start()
                context = {"success": True, "message": "Activity List","data": 'media/files/full-report.csv'}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {"success": False, "message": "state_id is missing"}
                return Response(context, status=status.HTTP_200_OK)

        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.',"error":str(error)}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def index(self, request,book_id,state_id):
        try:
            final_list = []
            import os
            from shutil import copyfile
            
            if book_id is not None:
                book_name=Book.objects.get(id=book_id)
                chapters=Chapter.objects.filter(book__id=book_id).order_by('id')
            else:
                chapters= Chapter.objects.filter(book__subject__grade__medium__state__id=state_id)
            serializer = OtherContentStatusSerializerdownload(chapters, many=True)
            for data in serializer.data:
                for d in data['chapter']:
                    final_list.append(d)

            data_frame = pd.DataFrame(final_list , columns=['Board', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Content name', 'School_name', 'Mobile', 'Email', 'File name','Status',"Content Type"])
            exists = os.path.isfile('full-report.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove('full-report.csv')
            # data_frame.to_excel(path + 'contentstatus.xlsx')
            data_frame.to_csv(path +'full-report.csv', encoding="utf-8-sig", index=False)
        except Exception as error:
            print(str(error))
            





class ApprovedOtherContentDownloadSecond(ListAPIView):
    queryset = Book.objects.all()

   

    def get(self,request):
        try:
            
            
            state_id = request.query_params.get('state', None)
            tag = request.query_params.get('tag',None)
            status_ = request.query_params.get('status',None)
            random_str = ''.join(random.choice(string.ascii_letters) for m in range(4))
            # random_str = "YGJAQ3"

            if Job.objects.filter(task_id=random_str).exists() is False:
                data = Job(task_id=random_str, status=False)
                data.save()
            else:
                exists.status = False
                exists.save()
            
            t = threading.Thread(target=self.index, args=(request,state_id,tag,status_,random_str), kwargs={})
            t.setDaemon(True)
            t.start()
            state_name=State.objects.get(id=state_id).state
            tag_name = Tags.objects.get(id=tag).tag_name
            if str(status_) == "approved":
                file_status = "Approved"
            else:
                file_status = "Rejected"
            if tag == "1":
                tag_name = "Content"
            context = {"success": True, "message": "Activity List", "id":random_str, "data": 'media/files/{}_{}_{}Contents.csv'.format(str(state_name),str(tag_name),str(file_status))}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Activity list.' ,"error" :str(error)}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def index(self, request,state_id,tag,status_,random_str):
        try:
            final_list = []
            chapters=Chapter.objects.filter(book__subject__grade__medium__state__id=state_id).order_by('id')
            file_status= ""
            if tag == "1":
                # import ipdb;ipdb.set_trace()
                serializer = ApprovedOtherContentSerializerBulkDownload(chapters, many=True,context={"status" : str(status_)})
                for data in serializer.data:
                    for d in data['chapter']:
                        final_list.append(d)
                if str(status_) == "approved":
                    file_status = "Approved"
                    data_frame1 = pd.DataFrame(final_list , columns=['Name of the Content',"Description of the content in one line - telling about the content",'Board','Class' ,'Medium', 'Subject', 'Textbook Name', 'Topic', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Resource Type','Keywords','Audience',"Creators",'Attribution (Credits)','icon','File format','Content Link/Video Link'])
 
            else:
                serializer = ApprovedOtherContentSerializerSecond(chapters, many=True,context={'tag_id':tag, "status" : str(status_)})
                for data in serializer.data:
                    for d in data['chapter']:
                        final_list.append(d)
                
                if str(status_) == "approved":
                    file_status = "Approved"
                    data_frame1 = (pd.DataFrame(final_list , columns=['Name of the Content',"Description of the content in one line - telling about the content",'Board','Class', 'Medium', 'Subject', 'Textbook Name', 'Topic', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','text','Resource Type','Keywords','Audience',"Creators",'Attribution (Credits)','icon','File format','Content Link/Video Link']))
                elif str(status_) == "rejected":
                    file_status = "Rejected"
                    data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Topic', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Content Name','Content Link/Video Link','text',"Creators",'Credit To','File format','Comment'])
                else:
                    data_frame1 = pd.DataFrame(final_list , columns=['Name of the Content',"Description of the content in one line - telling about the content",'Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Topic', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Content Link/Video Link','text',"Creators",'Attribution (Credits)','File format','Resource Type','Audience'])

                # repeat_list=['Content Name','Content Link/Video Link','text','linked_keywords']
                # data_frame1 = pd.DataFrame(final_list , columns=['Board', 'Medium', 'Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit', 'Keywords',]+(list(itertools.chain.from_iterable(itertools.repeat(repeat_list, 5)))))
            tag_name=""
            if tag == "10" or tag == "9":
                # video and pdf
                tag_name = Tags.objects.get(id=tag).tag_name
                df =(data_frame1.drop(['text','Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Textbook Name'], axis=1)).rename(index=str, columns={"Content Link/Video Link": "File path"})
                data_frame = df.drop_duplicates()
                # data_frame=data_frame_.rename(index=str, columns={"Content Link/Video Link": "Content Document Link","Content Name":"Question"})
            elif tag == "8":
                # question answer
                tag_name = Tags.objects.get(id=tag).tag_name
                df=(data_frame1.drop(['Content Link/Video Link','Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Textbook Name'], axis=1)).rename(index=str, columns={"Name of the Content": "Question","text":"Answer"})
                data_frame = df.drop_duplicates()
            elif tag == "7":
                # description
                tag_name = Tags.objects.get(id=tag).tag_name
                df=(data_frame1.drop(['Content Link/Video Link','Content Name','Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Textbook Name'], axis=1)).rename(index=str, columns={"text":"Learning Outcome Definition"})
                data_frame = df.drop_duplicates()
            elif tag == "11":
                # only pdf
                tag_name = Tags.objects.get(id=tag).tag_name
                df =(data_frame1.drop(['text','Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Textbook Name'], axis=1)).rename(index=str, columns={"Content Link/Video Link":"File path"})
                data_frame = df.drop_duplicates()
            elif tag == "1":
                tag_name = "Content"
                df=(data_frame1.drop(['Level 2 Textbook Unit', 'Level 3 Textbook Unit','Level 4 Textbook Unit','Textbook Name'], axis=1)).rename(index=str, columns={"Content Link/Video Link":"File path"})
                data_frame = df.drop_duplicates()
            else:
                data_frame=data_frame1
            state_name=State.objects.get(id=state_id).state
            exists = os.path.isfile(str(state_name)+"_"+str(tag_name)+'_'+file_status+'Contents.csv')
            path = settings.MEDIA_ROOT + '/files/'
            if exists:
                os.remove(str(state_name)+"_"+str(tag_name)+'_'+file_status+'Contents.csv')
            data_frame.to_csv(path + str(state_name) +"_"+str(tag_name)+'_'+file_status+'Contents.csv', encoding="utf-8-sig", index=False)

            t = Job.objects.get(task_id=random_str)
            t.status = True  # change field
            t.save()

        except Exception as e:
            print(str(e))
        

            


class JobStatus(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def get(self, request):
        try:
            task_id = request.query_params.get("id" , None)
            queryset = Job.objects.filter(task_id = task_id)
            serializer = JobSerializer(queryset, many=True)
            context = {"success": True, "message": "Job Status","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Job Status.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)