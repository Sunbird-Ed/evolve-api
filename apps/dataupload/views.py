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

import re
import os
import shutil
import glob
valid_columns = ['board', 'medium', 'grade', 'subject', 'textbook name', 'chapter name', 'chapter concept name in english','topic name', 'topic concept name in english','sub topic name','sub topic concept name in english','keywords in english']

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
                if i.get('level 3 textbook unit') is None:
                    i['level 3 textbook unit']=""
                    if i.get('level 2 textbook unit') is None:
                        i['level 2 textbook unit']=""
                
                
                state = State.objects.filter(id=state_id).first()
                # import ipdb;ipdb.set_trace()
                medium = Medium.objects.filter(medium__iexact=i['medium'], state=state).first()
                if medium is None:
                    Medium.objects.create(medium=i['medium'], state=state)
                medium = Medium.objects.filter(medium__iexact=i['medium'], state=state).first()
                
                grade = Grade.objects.filter(grade__iexact=i['grade'], medium=medium).first()
                if grade is None:
                    Grade.objects.create(grade=i['grade'], medium=medium)
                grade = Grade.objects.filter(grade__iexact=i['grade'], medium=medium).first()
               
                subject = Subject.objects.filter(Subject__iexact=i['subject'], grade=grade).first()
                if subject is None:
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
                context={"success": True, "message": "Excel Uploaded Successful", "error": ""}
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
                df = pd.read_csv(fs.path(file.name))
                json_list = df.to_dict('resource')
                context, res_status=self.upload(json_list, stateid)
                
            else:
                context = {"success": False, "message": "Please upload CSV OR EXCEL file", "error": ""}
                res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(context, status=res_status)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to create data.'}
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
            context = {"success": True, "message": "Chapter List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Chapter list.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request):
        try:
            serializer = Agegroupserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "message": "Created Successful", "error": "", "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
            error = serializer.errors['non_field_errors'][0].code
            if error == "unique":
                
               
                context = {"success": False, "message": "Age group already exist", "error": str(error)}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            context = {"success": False, "message": "Invalid Input Data to create Age Group", "error": str(serializer.errors)}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to create Age Group.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class ConvertTOCView(ListCreateAPIView):
    def check_compulsory_header(self,received_list):
        missing_col=[]
        board_synonyms = ['board']
        medium_synonyms = ['medium']
        grade_synonyms = ['grade']
        subject_synonyms = ['subject']
        book_synonyms = ['textbook name']
        if len(set(received_list)&set(board_synonyms)) == 0:
            missing_col.append("Board")
        if len(set(received_list)&set(medium_synonyms)) == 0:
            missing_col.append("Medium")
        if len(set(received_list)&set(grade_synonyms)) == 0:
            missing_col.append("Grade")
        if len(set(received_list)&set(subject_synonyms)) == 0:
            missing_col.append("Subject")
        if len(set(received_list)&set(book_synonyms)) == 0:
            missing_col.append("Textbook Name")
       
        return missing_col
   

    def missing_headers(self,received_list, acceptable_list):
        missing_col=[]
        board_synonyms = ['board']
        medium_synonyms = ['medium']
        grade_synonyms = ['grade']
        subject_synonyms = ['subject']
        book_synonyms = ['textbook name']
        chapter_synonyms = ['chapter name']
        section_synonyms = ['topic name']
        sub_section_synonyms = ['sub topic name']
        keywords_synonyms = ['keywords in english','keywords in english']
        chapter_mapped_topic_synonyms = ['chapter concept name in english']
        section_mapped_topic_synonyms = ['topic concept name in english']
        sub_section_mapped_topic_synonyms =['sub topic concept name in english']

        if len(set(received_list)&set(board_synonyms)) == 0:
            missing_col.append("Board")
        if len(set(received_list)&set(medium_synonyms)) == 0:
            missing_col.append("Medium")
        if len(set(received_list)&set(grade_synonyms)) == 0:
            missing_col.append("Grade")
        if len(set(received_list)&set(subject_synonyms)) == 0:
            missing_col.append("Subject")
        if len(set(received_list)&set(book_synonyms)) == 0:
            missing_col.append("Textbook Name")
        if len(set(received_list)&set(chapter_synonyms)) == 0:
            missing_col.append("Chapter Name")
        if len(set(received_list)&set(chapter_mapped_topic_synonyms)) == 0:
            missing_col.append("Chapter - Concept Name in English")
        if len(set(received_list)&set(section_synonyms)) == 0:
            missing_col.append("Topic name")
        if len(set(received_list)&set(section_mapped_topic_synonyms)) == 0:
            missing_col.append("Topic - Concept Name in English")
        if len(set(received_list)&set(sub_section_synonyms)) == 0:
            missing_col.append("Sub Topic Name")
        if len(set(received_list)&set(sub_section_mapped_topic_synonyms)) == 0:
            missing_col.append("Sub Topic - Concept Name in English")
        if len(set(received_list)&set(keywords_synonyms)) == 0:
            missing_col.append("Keywords in English")
        return missing_col

    def checkheader(self, received_list, acceptable_list,originalcolumns):
        unwanted_head=[]
        for notvalid in originalcolumns:
            if re.sub(' +', ' ', re.sub(r'[^a-zA-Z0-9]', ' ',notvalid).strip()).lower()  not in acceptable_list :
                unwanted_head.append(notvalid)
        valid_head=[]
    
        for valid in acceptable_list:
            for originalcolumn in originalcolumns:
                if valid == re.sub(' +', ' ', re.sub(r'[^a-zA-Z0-9]', ' ',originalcolumn).strip()).lower():
                    valid_head.append(originalcolumn)
        return unwanted_head, valid_head

    def convert(self, data):
        final_list= []
        board = str(data[0]['board'])
        grade = str(data[0]['grade'])
        medium = str(data[0]['medium'])
        subject = str(data[0]['subject'])
        book = str(data[0]['textbook name'])
        last_chapter_name = ""
        last_topic_name = ""
        for d in data:
            out_list = []
            current_chapter_name = d['chapter name']
            current_topic_name = d['topic name']
            if str(d['topic name']).lower() != "nan" and str(d['topic name']).lower() != "na":
                if str(d['sub topic name']).lower() != "nan" and str(d['sub topic name']).lower() != "na":
                    if last_chapter_name != str(current_chapter_name): 
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, "", "",  d['chapter concept name in english']])
                        final_list.append(out_list)
                        out_list=[]
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, d['topic name'], "",  d['topic concept name in english']])
                        final_list.append(out_list)
                        out_list=[]
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, d['topic name'], d['sub topic name'],  d['topic concept name in english'],d['keywords in english']])
                        final_list.append(out_list)
                        last_chapter_name = str(d['chapter name'])
                    elif last_chapter_name == str(current_chapter_name) and last_topic_name != current_topic_name:
                        out_list=[]
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, d['topic name'], "",  d['topic concept name in english']])
                        final_list.append(out_list)
                        out_list=[]
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, d['topic name'], d['sub topic name'],  d['sub topic concept name in english'],d['keywords in english']])
                        final_list.append(out_list)
                        last_topic_name = str(d['topic name'])

                    elif last_chapter_name == str(current_chapter_name) and last_topic_name == current_topic_name:
                        out_list=[]
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, d['topic name'], d['sub topic name'], d['sub topic concept name in english'], d['keywords in english']])
                        final_list.append(out_list)
                        last_chapter_name = str(d['chapter name'])


                else:
                    if last_chapter_name != str(current_chapter_name): 
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, "", "",  d['chapter concept name in english']])
                        final_list.append(out_list)
                        out_list=[]

                        last_chapter_name = current_chapter_name
                    if last_chapter_name == str(current_chapter_name):
                        if last_topic_name != str(current_topic_name):
                            out_list=[]
                            out_list.extend([board, medium, grade, subject, book])
                            out_list.extend([current_chapter_name, d['topic name'], "", d['topic concept name in english'], d['keywords in english']])
                            final_list.append(out_list)
                            last_topic_name = str(d['topic name'])

            else:
                if last_chapter_name != str(current_chapter_name): 
                        out_list.extend([board, medium, grade, subject, book])
                        out_list.extend([current_chapter_name, "", "", d['chapter concept name in english'], d['keywords in english']])
                        last_chapter_name = str(d['chapter name'])
                        final_list.append(out_list)
        return final_list



    def check_combination(self, df):
        check_througout=[]
        if len(set(df['board'])) != 1: 
            check_througout.append("Board")
        if len(set(df['medium'])) != 1:
            check_througout.append("Medium")
        if len(set(df['grade'])) != 1: 
            check_througout.append("Grade")
        if len(set(df['subject'])) != 1:
            check_througout.append("Subject")
        if len(set(df['textbook name'])) != 1:
            check_througout.append("Textbook Name")
        return check_througout

    def get_path_board_to_book(self, df):
        if len(set(df['board'])) == 1 and len(set(df['grade'])) == 1 and len(set(df['medium'])) == 1 and len(set(df['subject'])) == 1 and len(set(df['textbook name'])) == 1:
            
            data_list=(list(set(df['board'])) + list(set(df['medium'])) + list(set(df['grade'])) + list(set(df['subject'])) + list(set(df['textbook name'])))

            return "_".join(data_list )


    def valid_data(self, data):
        valid_data={}
       
        for key, value in data.items():
            key = re.sub(' +', ' ',key)
            key=key.lower()
            if type(value)==type(""):
                valid_data[key]= " ".join(str(value).split('\n')).strip()
            else:
                valid_data[key]=value

        return valid_data

    def post(self, request):
        try:

            uniform =  request.query_params.get('uniform', None)
            validate = request.query_params.get('validate', None)
            convert = request.query_params.get('convert', None)
            compulsory = request.query_params.get('compulsory', None)
            file = request.FILES.get('file')
            path = settings.MEDIA_ROOT + '/files/'
            fs = FileSystemStorage(location=path)
            pathconvertedfiles =settings.MEDIA_ROOT + '/files/convertedfiles/'
            filelist = glob.glob(os.path.join(pathconvertedfiles, "*.*"))
            for f in filelist:
                os.remove(f)
            if fs.exists(file.name):
                fs.delete(file.name)
            fs.save(file.name, file)
            
            if file.name.endswith('.xlsx'):
                xls = pd.ExcelFile(fs.path(file.name))
                df = pd.ExcelFile(fs.path(file.name))
                df = df.parse(xls.sheet_names[0], na_values=None)

                
                df.dropna()
                extracteddf=df[0:2000]
                df=extracteddf[list(extracteddf.columns[0:50] )]
                originalcolumns=df.columns 
                df.columns=[re.sub(' +', ' ', re.sub(r'[^a-zA-Z0-9]', ' ',x).strip()).lower() for x in df.columns]
            
                if validate is not None and validate == 'true':
                    unwanted_head, valid_col = self.checkheader(df.columns, valid_columns,originalcolumns)
                    missing_head=self.missing_headers(df.columns, valid_columns)
                    context={"success": True, "message": "checked", "unwanted_headers": unwanted_head, "missing_head" : missing_head, "acceptable_headers": valid_col}



                elif convert is not None and convert == 'true':
                    missing_head = self.missing_headers(df.columns, valid_columns)
                    for missing_header in missing_head:
                        if missing_header == 'Chapter Name':
                           df.insert(len(df.columns), "chapter name", "", True)
                        if missing_header == 'Topic name':
                           df.insert(len(df.columns), "topic name", "", True)
                        if missing_header == 'Sub Topic Name':
                           df.insert(len(df.columns), "sub topic name", "", True)
                        if missing_header == 'Chapter - Concept Name in English':
                           df.insert(len(df.columns), "chapter concept name in english", "", True)
                        if missing_header == 'Topic - Concept Name in English':
                           df.insert(len(df.columns), "topic concept name in english", "", True)
                        if missing_header == 'Sub Topic - Concept Name in English':
                           df.insert(len(df.columns), "sub topic concept name in english", "", True)
                        if missing_header == 'Keywords in English':
                           df.insert(len(df.columns), "keywords in english", "", True)
                    json_list = df.to_dict('resource')
                    out_list = self.convert(json_list)
                    data_frame = pd.DataFrame(out_list , columns=['Board', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'Mapped Topics','Keywords']).drop_duplicates()
                    path = settings.MEDIA_ROOT + '/files/convertedfiles/'
                    data_frame.to_csv(path + self.get_path_board_to_book(df)+".csv", encoding="utf-8-sig", index=False)
                    context = {'success': "true", 'message': 'combination matched', 'data': 'media/files/convertedfiles/{}'.format(self.get_path_board_to_book(df)+".csv")}
                elif uniform is not None and uniform == 'true':
                    data=self.check_combination(df)
                    if len(data) != 0  :
                        context = {'success': "false", 'message': 'data inconsistent', 'data': data}
                    else:
                        context = {'success': "true", 'message': 'data consistent', 'data': data}
                elif compulsory is not None and compulsory == 'true':
                    compulsory_missing = self.check_compulsory_header(df.columns)
                    if len(compulsory_missing)==0: 
                        context={"success": True, "message": "checked", "missing_head" : compulsory_missing}
                    else:
                        context={"success": False, "message": "checked", "missing_head" : compulsory_missing}

                else:
                    context = {'success': "false", 'message': '','error': str(error)}


                    



            elif file.name.endswith('.csv'):
                df = pd.read_csv(fs.path(file.name))
                originalcolumns=df.columns 
                df.columns=[re.sub(' +', ' ', re.sub(r'[^a-zA-Z0-9]', ' ',x).strip()).lower() for x in df.columns]
                if validate is not None and validate == 'true':
                    unwanted_head, valid_col = self.checkheader(df.columns, valid_columns,originalcolumns)
                    missing_head=self.missing_headers(df.columns, valid_columns)
                    context={"success": True, "message": "checked", "unwanted_headers": unwanted_head, "missing_head" : missing_head, "acceptable_headers": valid_col}
                elif convert is not None and convert == 'true':
                    missing_head = self.missing_headers(df.columns, valid_columns)
                    for missing_header in missing_head:
                        if missing_header == 'Chapter Name':
                           df.insert(len(df.columns), "chapter name", "", True)
                        if missing_header == 'Topic name':
                           df.insert(len(df.columns), "topic name", "", True)
                        if missing_header == 'Sub Topic Name':
                           df.insert(len(df.columns), "sub topic name", "", True)
                        if missing_header == 'Chapter - Concept Name in English':
                           df.insert(len(df.columns), "chapter concept name in english", "", True)
                        if missing_header == 'Topic - Concept Name in English':
                           df.insert(len(df.columns), "topic concept name in english", "", True)
                        if missing_header == 'Sub Topic - Concept Name in English':
                           df.insert(len(df.columns), "sub topic concept name in english", "", True)
                        if missing_header == 'Keywords in English':
                           df.insert(len(df.columns), "keywords in english", "", True)
                    json_list = df.to_dict('resource')
                    out_list = self.convert(json_list)
                    data_frame = pd.DataFrame(out_list , columns=['Board', 'Medium','Grade', 'Subject', 'Textbook Name', 'Level 1 Textbook Unit', 'Level 2 Textbook Unit', 'Level 3 Textbook Unit', 'Mapped Topics','Keywords'])
                    path = settings.MEDIA_ROOT + '/files/convertedfiles/'
                    filenamefordelete=self.get_path_board_to_book(df) +"_"+ os.path.splitext(file.name)[0]+".csv"
                    data_frame.to_csv(path + self.get_path_board_to_book(df) +".csv", encoding="utf-8-sig", index=False)
                    context = {'success': "true", 'message': 'combination matched', 'data': 'media/files/convertedfiles/{}'.format(self.get_path_board_to_book(df) +".csv")}
                elif uniform is not None and uniform == 'true':
                    data=self.check_combination(df)
                    if len(data) != 0  :
                        context = {'success': "false", 'message': 'data inconsistent', 'data': data}
                    else:
                        context = {'success': "true", 'message': 'data consistent', 'data': data}

                elif compulsory is not None and compulsory == 'true':
                    compulsory_missing = self.check_compulsory_header(df.columns)
                    if len(compulsory_missing)==0: 
                        context={"success": True, "message": "checked", "missing_head" : compulsory_missing}
                    else:
                        context={"success": False, "message": "checked", "missing_head" : compulsory_missing}
                else:

                    context = {'success': "false", 'message': '','error': str(error)}

            fs.delete(file.name)
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to check data.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)