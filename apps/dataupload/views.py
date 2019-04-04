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
from apps.configuration.models import State,Book,Medium,Grade,Subject
from .models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword
from .serializers import SubsectionNestedSerializer, SectionNestedSerializer, ChapterNestedSerializer, BookNestedSerializer
from .serializers import ChapterSerializer, SectionSerializer, SubSectionSerializer
from evolve import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd

@permission_classes((IsAuthenticated,))
class TOCUploadView(ListCreateAPIView):
    queryset = Chapter.objects.all()

    def valid_data(self, data):
        valid_data={}
        
       
        for key, value in data.items():
            key=key.lower()
            if type(value)==type(""):
                valid_data[key]= " ".join(str(value).split('\n')).strip()
            else:
                valid_data[key]=value

        return valid_data

    def upload(self, json_list, state_id):
        try:
            for i in json_list:
                i = self.valid_data(i)
                if i.get('level 4 textbook unit') is None:
                    i['level 4 textbook unit']=""
                    if i.get('level 3 textbook unit') is None:
                        i['level 3 textbook unit']=""
                        if i.get('level 2 textbook unit') is None:
                            i['level 2 textbook unit']=""
                
                
                state = State.objects.filter(id=state_id).first()
                if str(i['medium']).lower() != 'nan' and str(i['grade']).lower() != 'nan' and str(i['subject']).lower() != 'nan' and str(i['textbook name']).lower() != 'nan':
                    
                    medium = Medium.objects.filter(medium__iexact=i['medium'], state=state).first()
                    if medium is None:
                        Medium.objects.create(medium=i['medium'], state=state)
                    medium = Medium.objects.filter(medium__iexact=i['medium'], state=state).first()
                  
                    grade = Grade.objects.filter(grade__iexact=i['grade'], medium=medium).first()
                    if grade is None:
                        Grade.objects.create(grade=i['grade'], medium=medium)
                    grade = Grade.objects.filter(grade__iexact=i['grade'], medium=medium).first()
                   
                    subject = Subject.objects.filter(Subject__iexact=i['subject'], grade=grade).first()
                    if subject is None :
                        Subject.objects.create(Subject=i['subject'], grade=grade)
                    subject = Subject.objects.filter(Subject__iexact=i['subject'], grade=grade).first()
                   
                    book = Book.objects.filter(book=i['textbook name'], subject=subject).first()
                    if book is None:
                        Book.objects.create(book=i['textbook name'], subject=subject)
                    book = Book.objects.filter(book=i['textbook name'], subject=subject).first()
                    
                    chapter = Chapter.objects.filter(chapter=i['level 1 textbook unit'],book=book).first()
                    if chapter is None:
                        Chapter.objects.create(chapter=i['level 1 textbook unit'], book=book)
                    chapter = Chapter.objects.filter(chapter=i['level 1 textbook unit'], book=book).first()
                    
                    if str(i['level 2 textbook unit']).lower() != 'nan' and str(i['level 2 textbook unit']).lower() != '':           
                        section = Section.objects.filter(section=i['level 2 textbook unit'], chapter=chapter).first()
                        if section is None and i['level 2 textbook unit'] != "":
                            Section.objects.create(section=i['level 2 textbook unit'], chapter=chapter)
                    section = Section.objects.filter(section=i['level 2 textbook unit'], chapter=chapter).first()
                    
                    if i['level 3 textbook unit'] is not None and str(i['level 3 textbook unit']).lower() != 'nan' and str(i['level 3 textbook unit']).lower() != '':
                        sub_section = SubSection.objects.filter(sub_section=i['level 3 textbook unit'], section=section).first()
                        if sub_section is None and i['level 3 textbook unit'] != "":
                            SubSection.objects.create(sub_section=i['level 3 textbook unit'], section=section)
                    sub_section = SubSection.objects.filter(sub_section=i['level 3 textbook unit'], section=section).first()

                    if i['level 4 textbook unit'] is not None and str(i['level 4 textbook unit']).lower() != 'nan' and str(i['level 4 textbook unit']).lower() != '':
                        sub_sub_section = SubSubSection.objects.filter(sub_sub_section=i['level 4 textbook unit'], subsection=sub_section).first()
                        if sub_sub_section is None and i['level 4 textbook unit'] !="":
                            SubSubSection.objects.create(sub_sub_section=i['level 4 textbook unit'],subsection=sub_section)
                    sub_sub_section = SubSubSection.objects.filter(sub_sub_section=i['level 4 textbook unit'], subsection=sub_section).first()

                    if str(i['keywords']) != 'nan':
                        keyword_list = [x.strip() for x in i['keywords'].split(',')]
                        if str(i['level 1 textbook unit']).lower() != 'nan' and str(i['level 2 textbook unit']).lower() == 'nan':
                            for j in keyword_list:
                                if j !="":
                                    chapter_keyword = ChapterKeyword.objects.filter(chapter=chapter, keyword=j).first()
                                    if chapter_keyword is None:
                                        ChapterKeyword.objects.create(chapter=chapter, keyword=j)

                        elif str(i['level 2 textbook unit']).lower() != 'nan' and str(i['level 3 textbook unit']).lower() == 'nan' and str(i['level 2 textbook unit']).lower() != '':           
                            for j in keyword_list:
                                if j!="":
                                    section_keyword = SectionKeyword.objects.filter(section=section, keyword=j).first()
                                    if section_keyword is None:
                                        SectionKeyword.objects.create(section=section, keyword=j)

                        elif str(i['level 3 textbook unit']).lower() != 'nan' and str(i['level 4 textbook unit']).lower() != '' and str(i['level 4 textbook unit']).lower() == 'nan':
                            for j in keyword_list:
                                if j !="":
                                    sub_section_keyword = SubSectionKeyword.objects.filter(sub_section=sub_section, keyword=j).first()
                                    if sub_section_keyword is None:
                                        SubSectionKeyword.objects.create(sub_section=sub_section, keyword=j)

                        elif str(i['level 4 textbook unit']).lower() != 'nan' and str(i['level 4 textbook unit']).lower() != '':
                            for j in keyword_list:
                                if j !="":
                                    sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section=sub_sub_section, keyword=j).first()
                                    if sub_sub_section_keyword is None:
                                        SubSubSectionKeyword.objects.create(sub_sub_section=sub_sub_section, keyword=j)
                context={"success": True, "message": "File Uploaded Successful", "error": ""}
            res_status = status.HTTP_200_OK
            return context, res_status
                
        except Exception as error:

            context={"success": False, "message": "Upload Failed", "error": str(error)}
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return context, res_status

    def post(self, request):
        try:
            
            stateid=request.query_params.get("state",None)

            file = request.FILES.get('file')
            path = settings.MEDIA_ROOT + '/files/'
            fs = FileSystemStorage(location=path)
            if fs.exists(file.name):
                fs.delete(file.name)

            fs.save(file.name, file)

            if file.name.endswith('.xlsx'):
                
            
                xls = pd.ExcelFile(fs.path(file.name))
                xls.sheet_names
            
                sheet_to_df_map = {}
                for sheet_name in xls.sheet_names:
                    
                    df = pd.ExcelFile(fs.path(file.name))
                    df = df.parse(sheet_name, na_values=None)
                    columns = ['board','grade','subject','medium','book', 'chapter', 'section', 'sub_section' 'keywords', 'hard_spot', 'first_name', 'last_name', 'email', 'mobile', 'description', 'points_to_be_covered', 'useful_to', 'approval', 'comment rating', 'approved_by']
                
                    json_list = df.to_dict('resource')
                    context, res_status=self.upload(json_list , stateid)
                
            elif file.name.endswith('.csv'):
                df = pd.read_csv(fs.path(file.name),skipinitialspace=True)

                json_list = df.to_dict('resource')
                context, res_status=self.upload(json_list, stateid)
                
            else:
                context = {"success": False, "message": "Please upload CSV OR EXCEL file"}
                res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(context, status=res_status)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to create data.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     


class ChapterList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = ChapterSerializer
    def get(self, request):
        try:
            subject = request.query_params.get('subject', None)
            if subject is not None:
                queryset=self.get_queryset().filter(subject__id=subject)
            else:
                queryset = self.get_queryset()
            serializer = BookNestedSerializer(queryset, many=True)
            context = {"success": True, "message": "Chapter List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Chapter list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
