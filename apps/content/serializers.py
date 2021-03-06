from rest_framework import routers, serializers
from .models import Content,ContentContributors
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword,SubSubSection
from apps.configuration.models import Book,Grade,Subject
from apps.hardspot.models import HardSpot
from apps.hardspot.serializers import HardSpotCreateSerializer
from apps.othercontents.models import OtherContent 
from django.db.models import Q
from datetime import datetime, timedelta
import os
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
)
from evolve import settings
accountName = settings.AZURE_ACCOUNT_NAME
accountKey = settings.AZURE_ACCOUNT_KEY
containerName= settings.AZURE_CONTAINER
from datetime import datetime
from dateutil import tz
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Kolkata')

class ContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by=self.context.get('user', None)
        instance.rating = self.validated_data.get('rating', instance.rating)
        instance.rated_by = self.context.get('user', None)
        instance.comment = self.validated_data.get('comment', None)
        instance.save()
        return instance


class ContentStatusListSerializer(serializers.ModelSerializer):
    hard_spot = serializers.SerializerMethodField()
    sas_token=serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields=('id','hard_spot','content_name','video','approved','rating','comment','chapter','section','sub_section','approved_by','rated_by','content_contributors','chapter_keywords','section_keywords','sub_section_keywords','sas_token')

    def get_hard_spot(self, req):
        try:
            hardspot_data = HardSpot.objects.filter(id=req.hard_spot.id).first()
            serializer = HardSpotCreateSerializer(hardspot_data)
            data = serializer.data
            return data
        except:
            return None

    def get_sas_token(self,req):
        try:
            blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
            sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
            return sas_token
        except:
            return None
            
class SubSubSectionSerializer(serializers.ModelSerializer):
    contributions_count=serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()

    class Meta:
        model = SubSubSection
        fields = ['id',
        'subsection',
        'sub_sub_section',
        'contributions_count',
        'hardspot_count',
        'active'

        ]

    def get_hardspot_count(self,req):
        try:
            hardspot_count=HardSpot.objects.filter(sub_sub_section_id=req.id, approved=True).count()
            return hardspot_count
        except:
            return None
    def get_contributions_count(self,req):
        try:
            contributions_approved=Content.objects.filter(sub_sub_section_id=req.id,approved=True).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(sub_sub_section_id=req.id,approved=False,approved_by=None).count()
            return (contributions_approved + contributions_pending)
        except:
            return None


    

class SubSectionSerializer(serializers.ModelSerializer):
    contributions_count=serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()
    sub_sub_section=serializers.SerializerMethodField()
    class Meta:
        model = SubSection
        fields = ['id',
        'section',        
        'sub_section',
        'contributions_count',
        'hardspot_count',
        'sub_sub_section',
        'active'

        ]
    def get_hardspot_count(self,req):
        try:
            hardspot_count=HardSpot.objects.filter(sub_section_id=req.id, approved=True).count()
            return hardspot_count
        except:
            return None
    def get_contributions_count(self,req):
        try:
            contributions_approved=Content.objects.filter(sub_section_id=req.id,approved=True).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(sub_section_id=req.id,approved=False,approved_by=None).count()
            return (contributions_approved + contributions_pending)
        except:
            return None
    def get_sub_sub_section(self,req):
        try:
            sub_sub_section_data = SubSubSection.objects.filter(subsection=req.id).order_by('id')
            serializer = SubSubSectionSerializer(sub_sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None





class SectionNestedSerializer(serializers.ModelSerializer):
    sub_section = serializers.SerializerMethodField()
    contributions_count=serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()
    class Meta:
        model = Section
        fields = ['id',
                'section',
                'sub_section',
                'contributions_count',
                'hardspot_count',
                'active']

    def get_sub_section(self, req):
        try:
            sub_section_data = SubSection.objects.filter(section=req.id).order_by('id')
            serializer = SubSectionSerializer(sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None
    def get_hardspot_count(self,req):
        try:
            hardspot_count=HardSpot.objects.filter(section_id=req.id, approved=True).count()
            return hardspot_count
        except:
            return None
    def get_contributions_count(self,req):
        try:
            contributions_approved=Content.objects.filter(section_id=req.id,approved =True).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(section_id=req.id,approved=False,approved_by=None).count()
            return (contributions_approved + contributions_pending)
        except:
            return None 

class SubsectionNestedSerializer(serializers.ModelSerializer):
    sub_section = SectionNestedSerializer()
    total=serializers.SerializerMethodField()

    class Meta:
        model = SubSection
        fields = ['id',
                'section',
                'sub_section',]

class ChapterNestedSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()
    contributions_count=serializers.SerializerMethodField()


    class Meta:
        model = Chapter
        fields =['id','chapter','section','hardspot_count','contributions_count','active']

    def get_hardspot_count(self,req):
        try:
            hardspot_count=HardSpot.objects.filter(chapter_id=req.id, approved=True).count()
            return hardspot_count
        except:
            return None
    def get_contributions_count(self,req):
        try:
            contributions_approved=Content.objects.filter(chapter_id=req.id,approved=True).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(chapter_id=req.id,approved=False,approved_by=None).count()
            return (contributions_approved + contributions_pending)
        except:
            return None       

    def get_section(self, req):
        try:
            section_data = Section.objects.filter(chapter=req.id).order_by('id')
            serializer = SectionNestedSerializer(section_data, many=True)
            data = serializer.data
            return data
        except:
            return None

class BookNestedSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id',
                'book',
                'subject',
                'chapter',  
                ]
    def get_chapter(self, req):
        try:
            chapter_data = Chapter.objects.filter(book=req.id).order_by('id')
            serializer = ChapterNestedSerializer(chapter_data, many=True)
            data = serializer.data
            return data
        except:
            return None
#<------------------------------------------------------------------>
class ContentSubSubSectionSerializer(serializers.ModelSerializer):
    total=serializers.SerializerMethodField()
    approved=serializers.SerializerMethodField()
    reject=serializers.SerializerMethodField()
    pending=serializers.SerializerMethodField()

    class Meta:
        model = SubSubSection
        fields = ['id',
        'sub_sub_section',
        'total',
        'approved',
        'reject',
        'pending',
        ]


    
    def get_total(self, req):
        try:
            count = Content.objects.filter(sub_sub_section=req.id).count()
            return count
        except:
            return None

    def get_approved(self, req):
        try:
            sub_sec_approved = Content.objects.filter(approved=True,sub_sub_section=req.id).count()
            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            sub_sec_reject = Content.objects.filter(approved=False,sub_sub_section=req.id).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sub_sec_pending = Content.objects.filter(approved=False,sub_sub_section=req.id,approved_by=None).count()
            return sub_sec_pending
        except:
            return None



class ContentSubSectionSerializer(serializers.ModelSerializer):
    total=serializers.SerializerMethodField()
    approved=serializers.SerializerMethodField()
    reject=serializers.SerializerMethodField()
    pending=serializers.SerializerMethodField()
    sub_sub_section=serializers.SerializerMethodField()

    class Meta:
        model = SubSection
        fields = ['id',
        'sub_section',
        'total',
        'approved',
        'reject',
        'pending',
        'sub_sub_section',
        ]




    def get_sub_sub_section(self, req):
        try:
            sub_section_data = SubSubSection.objects.filter(subsection=req.id).order_by('id')
            serializer = ContentSubSubSectionSerializer(sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None

    
    def get_total(self, req):
        try:
            count = Content.objects.filter(sub_section=req.id).count()
            return count
        except:
            return None

    def get_approved(self, req):
        try:
            sub_sec_approved = Content.objects.filter(approved=True,sub_section=req.id).count()
            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            sub_sec_reject = Content.objects.filter(approved=False,sub_section=req.id).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sub_sec_pending = Content.objects.filter(approved=False,sub_section=req.id,approved_by=None).count()
            return sub_sec_pending
        except:
            return None



class ContentSectionNestedSerializer(serializers.ModelSerializer):
    sub_section = serializers.SerializerMethodField()
    total=serializers.SerializerMethodField()
    approved=serializers.SerializerMethodField()
    reject=serializers.SerializerMethodField()
    pending=serializers.SerializerMethodField()
    class Meta:
        model = Section
        fields = ['id',
                'section',
                'total',
                'approved',
                'reject',
                'pending',
                'sub_section',]



    def get_sub_section(self, req):
        try:
            sub_section_data = SubSection.objects.filter(section=req.id).order_by('id')
            serializer = ContentSubSectionSerializer(sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None
    def get_total(self, req):
        try:
            count = Content.objects.filter(section=req.id).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            sec_approved = Content.objects.filter(approved=True,section=req.id).count()
            return sec_approved
        except:
            return None
    def get_reject(self, req):
        try:
            sec_reject = Content.objects.filter(approved=False,section=req.id).exclude(approved_by=None).count()
            return sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sec_pending = Content.objects.filter(approved=False,section=req.id,approved_by=None).count()
            return sec_pending
        except:
            return None



class ContentChapterNestedSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    total=serializers.SerializerMethodField()
    approved=serializers.SerializerMethodField()
    reject=serializers.SerializerMethodField()
    pending=serializers.SerializerMethodField()
   

    class Meta:
        model = Chapter
        fields =['id','chapter','total','approved','reject','pending','section']



    def get_section(self, req):
        try:
            section_data = Section.objects.filter(chapter=req.id).order_by('id')
            serializer = ContentSectionNestedSerializer(section_data, many=True)
            data = serializer.data
            return data
        except:
            return None

    def get_total(self, req):
        try:
            count = Content.objects.filter(chapter=req.id).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            chapter_approved = Content.objects.filter(approved=True,chapter=req.id).count()
            return chapter_approved
        except:
            return None
    def get_reject(self, req):
        try:
            chapter_reject = Content.objects.filter(approved=False,chapter=req.id).exclude(approved_by=None).count()
            return chapter_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            chapter_pending = Content.objects.filter(approved=False,chapter=req.id,approved_by=None).count()
            return chapter_pending
        except:
            return None





class BookListSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id',
                'book',
                'subject',
                'chapter',  
                ]
    def get_chapter(self, req):
        try:
            chapter_data = Chapter.objects.filter(book=req.id).order_by('id')
            serializer = ContentChapterNestedSerializer(chapter_data, many=True)
            data = serializer.data
            return data
        except:
            return None
# <--------------------------------------------------------------------------->
class ChapterKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChapterKeyword
        fields='__all__'

class SectionKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SectionKeyword
        fields='__all__'

class SubSectionKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubSectionKeyword
        fields='__all__'

class SubSubSectionKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubSubSectionKeyword
        fields='__all__'


class KeywordSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField()
    hard_spot = serializers.SerializerMethodField()
    content_contributors = serializers.SerializerMethodField()
    sas_token=serializers.SerializerMethodField()
    class Meta:
        model = Content
        fields = ('id','hard_spot','chapter','section','sub_section','content_name','video','approved','approved_by' ,'rating','rated_by','comment','keywords', 'content_contributors','sas_token')
    
    def get_sas_token(self,req):
        try:
            blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
            sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
            return sas_token
        except:
            return None

    def get_hard_spot(self, req):
        try:
            hardspot_data = HardSpot.objects.filter(id=req.hard_spot.id).first()
            serializer = HardSpotCreateSerializer(hardspot_data)
            data = serializer.data
            return data
        except:
            return None

    def get_keywords(self, obj):
        try:
            if obj.chapter_keywords.all().exists():
                k=obj.chapter_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = ChapterKeywordsSerializer(ChapterKeyword.objects.filter(keyword__in=listValues, chapter__id=obj.chapter_id), many=True)
                return serializer.data
            elif obj.section_keywords.all().exists():
                k=obj.section_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = SectionKeywordsSerializer(SectionKeyword.objects.filter(keyword__in=listValues, section__id=obj.section_id), many=True)
                return serializer.data
            elif obj.sub_section_keywords.all().exists():
                k=obj.sub_section_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = SubSectionKeywordsSerializer(SubSectionKeyword.objects.filter(keyword__in=listValues, sub_section__id=obj.sub_section_id), many=True)
                return serializer.data
            elif obj.sub_sub_section_keywords.all().exists():
                k=obj.sub_sub_section_keywords.all().values('keyword')
                listData = [x for x in k ]
                print(listData)
                listValues = []
                for keyvalues in listData:
                    listValues.append(keyvalues['keyword'])
                print(listValues)
                serializer = SubSubSectionKeywordsSerializer(SubSubSectionKeyword.objects.filter(keyword__in=listValues, sub_sub_section__id=obj.sub_sub_section_id), many=True)
                return serializer.data
            else:
                return None
        except Exception as error:
            pass

    def get_content_contributors(self, req):
        try:
            content_contributor = ContentContributors.objects.filter(id=req.content_contributors.id).first()
            serializer = ContentContributorSerializer(content_contributor)
            data = serializer.data
            return data
        except:
            return None


class SectionKeywordSerializer(serializers.ModelSerializer):
    section_keywords=SectionKeywordsSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Content
        fields = ('section_keywords',)

class SubSectionKeywordSerializer(serializers.ModelSerializer):
    sub_section_keywords=SubSectionKeywordsSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ('sub_section_keywords',)


class ContentContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentContributors
        fields='__all__'





class ContentDownloadSerializer(serializers.ModelSerializer):
    selected_keyword = serializers.SerializerMethodField()
    class Meta:
        model=Content
        fields=('content_name','video','rating','comment', 'selected_keyword')

    def get_selected_keyword(self, obj):
        if  obj.chapter_keywords.all().count() != 0:
            linked_keyword = ChapterKeyword.objects.filter(id__in=obj.chapter_keywords.all())
            keyword_list=','.join([str(x.keyword) for x in linked_keyword.all()])
            return keyword_list
        elif obj.section_keywords.all().count() != 0:
            linked_keyword = SectionKeyword.objects.filter(id__in=obj.section_keywords.all())
            keyword_list=','.join([str(x.keyword) for x in linked_keyword.all()])
            return keyword_list
        elif obj.sub_section_keywords.all().count() != 0:
            linked_keyword = SubSectionKeyword.objects.filter(id__in=obj.sub_section_keywords.all())
            keyword_list=','.join([str(x.keyword) for x in linked_keyword.all()])
            return keyword_list
        elif obj.sub_sub_section_keywords.all().count() != 0:
            linked_keyword = SubSubSectionKeyword.objects.filter(id__in=obj.sub_sub_section_keywords.all())
            keyword_list=','.join([str(x.keyword) for x in linked_keyword.all()])
            return keyword_list
        else:
            return None

class ApprovedContentSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
   
    class Meta:
        model = Chapter
       
        fields = ['chapter']

    def getkeywords(self, keywords):
        keyword = ""
        for keys in keywords:
            keyword =  keyword + keys.keyword + ", "
        return keyword    

    def get_chapter(self, req):
        data_str_list = []
       
        chapters=Chapter.objects.filter(id=req.id).first()
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        if self.context['status'] == "approved": 
            chapter_content = Content.objects.filter(chapter__id=chapters.id,approved=True)
        elif self.context['status'] == "rejected":
            chapter_content = Content.objects.filter(chapter__id=chapters.id,approved=False).exclude(approved_by=None)
        else:
            chapter_content = Content.objects.filter(chapter__id=chapters.id,approved=True)
        section, sub_section, sub_sub_section, content_name,file_url, keyword, keyword_list = "","","","","","",""
        chapter_keyword = ChapterKeyword.objects.filter(chapter__id=chapters.id)
        if chapter_content.exists():
            for chapter_content_data in chapter_content:
                if  chapter_content_data.chapter_keywords.all().count() != 0:
                    linked_keyword = ChapterKeyword.objects.filter(id__in=chapter_content_data.chapter_keywords.all())
                    keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                    
                else:
                    keyword_list = ""
                keyword=self.getkeywords(chapter_keyword)
                tempList = tempList + [section,sub_section,sub_sub_section,keyword,chapter_content_data.content_name,chapter_content_data.video]
                keyword = ""

                lastname=ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).last_name
                if lastname is None  :
                    lastname=""
                tempList.append(str(ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).first_name) + " "+ lastname  )
                school_name=ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).school_name
                if school_name is None:
                    school_name = ""
                # tempList.append(school_name) 
                fileurl = chapter_content_data.video
                if fileurl is not None and fileurl !="" :
                    path,ext = os.path.splitext(fileurl)
                    ext = ext.replace(".","").strip()
                    if str(ext)== "mp4" or str(ext) == "pdf":
                        tempList.append(ext)
                    else:
                        tempList.append("")
                else:
                    tempList.append("")
                if self.context['status']=="rejected":
                    tempList.append(chapter_content_data.comment)
                tempList.append(keyword_list)
                data_str_list.append( tempList)
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        else:
            keyword=self.getkeywords(chapter_keyword)
            tempList = tempList + [section,sub_section,sub_sub_section,keyword]
            keyword = ""
            for _ in range(5):
                tempList.append("")
            if self.context['status']=="rejected":
                    tempList.append("")
            data_str_list.append( tempList )
            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]


        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]

        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            for section_data in sections:
                sections_1 = (section_data.section)
                if self.context['status'] == "approved":
                    sec_content = Content.objects.filter(section__id=section_data.id,approved=True)
                elif self.context['status'] == "rejected":
                    sec_content = Content.objects.filter(section__id=section_data.id,approved=False).exclude(approved_by=None)
                else:
                    sec_content = Content.objects.filter(section__id=section_data.id,approved=True)
                sub_section,sub_sub_section,content_name,file_url,keyword,keyword_list = "","","","","",""
                section_keyword = SectionKeyword.objects.filter(section__id=section_data.id)
              

                if sec_content.exists():
                    for section_content_data in sec_content:
                        keyword=self.getkeywords(section_keyword)
                        if  section_content_data.section_keywords.all().count() != 0:
                            linked_keyword = SectionKeyword.objects.filter(id__in=section_content_data.section_keywords.all())
                            keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                            
                        else:
                            keyword_list = ""
                        tempList = tempList + [sections_1,sub_section,sub_sub_section,keyword,section_content_data.content_name,section_content_data.video]
                        keyword=""
                        lastname=ContentContributors.objects.get(id=section_content_data.content_contributors_id).last_name
                        if lastname is None  :
                            lastname=""
                        tempList.append(str(ContentContributors.objects.get(id=section_content_data.content_contributors_id).first_name) + " "+ str(lastname)  )
                        school_name = ContentContributors.objects.get(id=section_content_data.content_contributors_id).school_name
                        if school_name is None or school_name == "":
                            school_name = ""
                        fileurl = section_content_data.video
                        if fileurl is not None and fileurl !="" :
                            path,ext = os.path.splitext(fileurl)
                            ext = ext.replace(".","").strip()
                            if str(ext)== "mp4" or str(ext) == "pdf":
                                tempList.append(ext)
                            else:
                                tempList.append("")
                        else:
                            tempList.append("")
                        tempList.append(keyword_list)
                        if self.context['status']=="rejected":
                            tempList.append(section_content_data.comment)
                        data_str_list.append( tempList )
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, ]
                else:
                    keyword = self.getkeywords(section_keyword)
                    tempList = tempList + [sections_1,sub_section ,sub_sub_section,keyword]
                    keyword=""
                    for _ in range(5):
                        tempList.append("")
                    if self.context['status']=="rejected":
                        tempList.append("")
      
                    data_str_list.append( tempList )
                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]

                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter , section_data.section]

                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        sub_sections=sub_section_data.sub_section 
                        sub_sub_section,content_name,file_url,keyword,keyword_list = "","","","",""

                        sub_section_keyword = SubSectionKeyword.objects.filter(sub_section__id=sub_section_data.id)
                        if self.context['status'] == "approved":
                            sub_sec_content = Content.objects.filter(sub_section__id=sub_section_data.id,approved=True)
                        elif self.context['status'] == "rejected":
                            sub_sec_content = Content.objects.filter(sub_section__id=sub_section_data.id,approved=False).exclude(approved_by=None)
                        else:
                            sub_sec_content = Content.objects.filter(sub_section__id=sub_section_data.id,approved=True)
                        if sub_sec_content.exists():
                            for sub_section_content_data in sub_sec_content:
                                keyword = self.getkeywords(sub_section_keyword)
                                if  sub_section_content_data.sub_section_keywords.all().count() != 0:
                                    linked_keyword = SubSectionKeyword.objects.filter(id__in=sub_section_content_data.sub_section_keywords.all())
                                    keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                                    
                                else:
                                    keyword_list = ""
                                
                                tempList = tempList + [sub_sections,sub_sub_section,keyword,sub_section_content_data.content_name,sub_section_content_data.video]
                                keyword = ""
                                lastname=ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).last_name
                                if lastname is None  :
                                    lastname=""
                                tempList.append(str(ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                school_name  = ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).school_name
                                if school_name is None or school_name == "":
                                    school_name = ""
                                # tempList.append(school_name)
                                fileurl = sub_section_content_data.video
                                if fileurl is not None and fileurl !="" :
                                    path,ext = os.path.splitext(fileurl)
                                    ext = ext.replace(".","").strip()
                                    if str(ext)== "mp4" or str(ext) == "pdf":
                                        tempList.append(ext)
                                    else:
                                        tempList.append("")
                                else:
                                    tempList.append("")
                                if self.context['status']=="rejected":
                                    tempList.append(sub_section_content_data.comment)
                                tempList.append(keyword_list)
                                
                                data_str_list.append( tempList )
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                        else:
                            keyword = self.getkeywords(sub_section_keyword)
                            tempList = tempList + [sub_sections,sub_sub_section,keyword]
                            keyword = ""
                            for _ in range(5):
                                tempList.append("")
                            if self.context['status']=="rejected":
                                tempList.append("")

                
                            data_str_list.append( tempList )
                            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]

                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section in sub_sub_sections:
                                sub_sub_sections_1=( sub_sub_section.sub_sub_section )
                                keyword = ""
                                sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section__id=sub_sub_section.id)
                                if self.context['status'] == "approved":
                                    sub_sub_sec_content = Content.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True)
                                elif self.context['status'] == "rejected":
                                    sub_sub_sec_content = Content.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=False).exclude(approved_by=None)
                                else:
                                    sub_sub_sec_content = Content.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True)
                                if sub_sub_sec_content.exists():
                                   for sub_sub_sec_content_data in sub_sub_sec_content:
                                        keyword = self.getkeywords(sub_sub_section_keyword)
                                        if  sub_sub_sec_content_data.sub_sub_section_keywords.all().count() != 0:
                                            linked_keyword = SubSubSectionKeyword.objects.filter(id__in=sub_sub_sec_content_data.sub_sub_section_keywords.all())
                                            keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                                            
                                        else:
                                            keyword_list = ""
                                        tempList = tempList + [sub_sub_sections_1,keyword,sub_sub_sec_content_data.content_name,sub_sub_sec_content_data.video]
                                        keyword = ""
                                        lastname=ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).last_name
                                        if lastname is None  :
                                            lastname=""
                                        tempList.append(str(ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                        school_name = ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).school_name
                                        if school_name is None or school_name == "":
                                            school_name = ""
                                        fileurl = sub_sub_sec_content_data.video
                                        if fileurl is not None and fileurl !="" :
                                            path,ext = os.path.splitext(fileurl)
                                            ext = ext.replace(".","").strip()
                                            if str(ext) == "mp4" or str(ext) == "pdf":
                                                tempList.append(ext)
                                            else:
                                                tempList.append("")
                                        else:
                                            tempList.append("")
                                        if self.context['status']=="rejected":
                                            tempList.append(sub_sub_sec_content_data.comment)
                                        tempList.append(keyword_list)                
                                        data_str_list.append( tempList )
                                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]

                                else:
                                    keyword = self.getkeywords(sub_sub_section_keyword)
                                    tempList = tempList + [sub_sub_sections_1,keyword]
                                    keyword = ""
                                    for _ in range(5):
                                        tempList.append("")
                                    if self.context['status']=="rejected":
                                        tempList.append("")
                                    data_str_list.append( tempList )
                                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
        
        return data_str_list


class ContentStatusSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
    class Meta:
        model = Chapter
        fields = ['chapter']
    
    def get_chapter(self, req):
        data_str_list = []
        # import ipdb;ipdb.set_trace()
        chapters=Chapter.objects.filter(id=req.id).first()
        # chapters=Chapter.objects.filter(id=req.id).first()
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        section = " "
        sub_section = " "
        sub_sub_section = " "
        tempList.append(sub_sub_section)
        tempList.append(section)
        tempList.append(sub_section)
        total = Content.objects.filter(chapter__id=chapters.id).count()
        approved = Content.objects.filter(chapter__id=chapters.id, approved=True).count()
        rejected = Content.objects.filter(chapter__id=chapters.id, approved=False).exclude(approved_by=None).count()
        pending = Content.objects.filter(chapter__id=chapters.id, approved=False, approved_by=None).count()
        hard_spot = HardSpot.objects.filter(chapter__id=chapters.id).count()
        tempList.append(total)
        tempList.append(approved)
        tempList.append(rejected)
        tempList.append(pending)
        tempList.append(hard_spot)
        data_str_list.append( tempList)
        # print("1:>>"+str(len(tempList)))
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            for section_data in sections:
                tempList.append( section_data.section )
                sub_section = " "
                tempList.append(sub_section)
                sub_sub_section = " "
                tempList.append(sub_sub_section)
                total = Content.objects.filter(section__id=section_data.id).count()
                approved = Content.objects.filter(section__id=section_data.id, approved=True).count()
                rejected = Content.objects.filter(section__id=section_data.id, approved=False).exclude(approved_by=None).count()
                pending = Content.objects.filter(section__id=section_data.id, approved=False, approved_by=None).count()
                hard_spot = HardSpot.objects.filter(section__id=section_data.id).count()
                tempList.append(total)
                tempList.append(approved)
                tempList.append(rejected)
                tempList.append(pending)
                tempList.append(hard_spot)
                data_str_list.append( tempList )
                # print("2:>>"+str(len(tempList)))

                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]

                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        tempList.append( sub_section_data.sub_section )
                        sub_sub_section = " "
                        tempList.append(sub_sub_section)
                        total = Content.objects.filter(sub_section__id=sub_section_data.id).count()
                        approved = Content.objects.filter(sub_section__id=sub_section_data.id, approved=True).count()
                        rejected = Content.objects.filter(sub_section__id=sub_section_data.id, approved=False).exclude(approved_by=None).count()
                        pending = Content.objects.filter(sub_section__id=sub_section_data.id, approved=False, approved_by=None).count()
                        hard_spot = HardSpot.objects.filter(sub_section__id=sub_section_data.id).count()
                        tempList.append(total)
                        tempList.append(approved)
                        tempList.append(rejected)
                        tempList.append(pending)
                        tempList.append(hard_spot)
                        data_str_list.append( tempList )
                        # print("3:>>"+str(len(tempList)))                       
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section_data in sub_sub_sections:
                                tempList.append(sub_sub_section_data.sub_sub_section)
                                total = Content.objects.filter(sub_sub_section__id=sub_sub_section_data.id).count()
                                approved = Content.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=True).count()
                                rejected = Content.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=False).exclude(approved_by=None).count()
                                pending = Content.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=False, approved_by=None).count()
                                hard_spot = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id).count()
                                tempList.append(total)
                                tempList.append(approved)
                                tempList.append(rejected)
                                tempList.append(pending)
                                tempList.append(hard_spot)
                                data_str_list.append( tempList )

                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
    
        return data_str_list
    


class ContentContributorsSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    city_name=serializers.SerializerMethodField()
    school_name=serializers.SerializerMethodField()
    textbook_name=serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['first_name',
                'last_name',
                'mobile',
                'email',
                'city_name',
                'school_name',
                'textbook_name',
                'grade',
                'subject']
    def get_first_name(self, obj):
        try:
            first_name=ContentContributors.objects.filter(id=obj.content_contributors.id).first().first_name
            return first_name
        except Exception as error:
            return None
    def get_last_name(self, obj):
        try:
            last_name=ContentContributors.objects.filter(id=obj.content_contributors.id).first().last_name
            return last_name
        except Exception as e:
            return None
    def get_mobile(self, obj):
        mobile=ContentContributors.objects.filter(id=obj.content_contributors.id).first().mobile
        return mobile
    def get_email(self, obj):
        try:
        
            email=ContentContributors.objects.filter(id=obj.content_contributors.id).first().email
            return email
        except Exception as e:
            return None
    def get_school_name(self ,obj):
        try:
            school_name=ContentContributors.objects.filter(id=obj.content_contributors.id).first().school_name
            return school_name
        except Exception as e:
            return None
    def get_city_name(self,obj):
        try:
            city_name = ContentContributors.objects.filter(id=obj.content_contributors.id).first().city_name
            return city_name
        except Exception as e:
            return None
    def get_textbook_name(self, obj):
        if obj.chapter is not None:
            book = Book.objects.filter(id=obj.chapter.book.id)
            books=','.join([str(x.book) for x in book.all()])
            return books
        elif obj.section is not None:
            book = Book.objects.filter(id=obj.section.chapter.book.id)
            books=','.join([str(x.book) for x in book.all()])
            return books
        elif obj.sub_section is not None:
            book = Book.objects.filter(id = obj.sub_section.section.chapter.book.id)
            books=','.join([str(x.book) for x in book.all()])
            return books
        elif obj.sub_sub_section is not None:
            book = Book.objects.filter(id = obj.sub_sub_section.subsection.section.chapter.book.id)
            books=','.join([str(x.book) for x in book.all()])
            return books
        else:
            return None


    def get_grade(self, obj):

        if obj.chapter is not None:
            grade = Grade.objects.filter(id=obj.chapter.book.subject.grade.id )
            grades = ','.join([str(x.grade) for x in grade.all()])
            return grades
        elif obj.section is not None:
            grade = Grade.objects.filter(id=obj.section.chapter.book.subject.grade.id)
            grades=','.join([str(x.grade) for x in grade.all()])
            return grades
        elif obj.sub_section is not None:
            grade = Grade.objects.filter(id = obj.sub_section.section.chapter.book.subject.grade.id)
            grades=','.join([str(x.grade) for x in grade.all()])
            return grades
        elif obj.sub_sub_section is not None:
            grade = Grade.objects.filter(id = obj.sub_sub_section.subsection.section.chapter.book.subject.grade.id)
            grades = ','.join([str(x.grade) for x in grade.all()])
            return grades
        else:
            return None

    def get_subject(self, obj):
        if obj.chapter is not None:
            subject = Subject.objects.filter(id=obj.chapter.book.subject.id )
            subjects = ','.join([str(x.Subject) for x in subject.all()])
            return subjects
        elif obj.section is not None:
            subject = Subject.objects.filter(id=obj.section.chapter.book.subject.id)
            subjects=','.join([str(x.Subject) for x in subject.all()])
            return subjects
        elif obj.sub_section is not None:
            subject = Subject.objects.filter(id = obj.sub_section.section.chapter.book.subject.id)
            subjects=','.join([str(x.Subject) for x in subject.all()])
            return subjects
        elif obj.sub_sub_section is not None:
            subject = Subject.objects.filter(id = obj.sub_sub_section.subsection.section.chapter.book.subject.id)
            subjects = ','.join([str(x.Subject) for x in subject.all()])
            return subjects
        else:
            return None


class ApprovedOtherContentSerializerBulkDownload(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
    
    class Meta:
        model = Chapter
        fields = ['chapter']
    
    def getkeywords(self, keywords):
        keyword = ""
        for keys in keywords:
            keyword =  keyword + keys.keyword + ", "
        return keyword

    def convert_utc_to_ist(self,utc):
        _utc = utc.strftime("%Y-%m-%d %H:%M:%S")
        _utc_fmt = datetime.strptime(_utc, '%Y-%m-%d %H:%M:%S')
        created_ist_ = _utc_fmt.replace(tzinfo=from_zone)
        _ist = created_ist_.astimezone(to_zone)
        return _ist.strftime("%Y-%m-%d %H:%M:%S")

    def get_chapter(self, req):
        data_str_list = []
        chapters=Chapter.objects.filter(id=req.id).first()
        chapter_ = (chapters.chapter).split("(")
        if (len(chapter_)>1) :
            chapter = (chapter_[1].replace(")",""))
            chapter = ""
        else:
            chapter = ""
        chapter =""
        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book ,chapter]
        if self.context['status'] == "approved":
            chapter_content = Content.objects.filter(chapter__id=chapters.id,approved=True).order_by("id")
        section, sub_section, sub_sub_section, content_name,file_url, text, keyword, keyword_list = "","","","","","","",""
        chapter_keyword = ChapterKeyword.objects.filter(chapter__id=chapters.id).order_by("id")
        
        if chapter_content.exists(): 
            for chapter_content_data in chapter_content:
                if  chapter_content_data.chapter_keywords.all().count() != 0:
                    linked_keyword = ChapterKeyword.objects.filter(id__in=chapter_content_data.chapter_keywords.all())
                    keyword =','.join([str(x.keyword) for x in linked_keyword.all()])
                    
                else:
                    keyword = ""
                tempList = [chapter_content_data.content_name,"This resource is about "+str(chapters.book)+","+str(chapters.chapter)] + tempList + [section,sub_section,sub_sub_section,]
                tempList.append("Learn")
                tempList.append(keyword)
                tempList.append("Learner")
                lastname=ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).last_name
                if lastname is None  :
                    lastname=""
                tempList.append(str(ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).first_name) + " "+ lastname  )
                tempList.append(ContentContributors.objects.get(id=chapter_content_data.content_contributors_id).school_name) 
                tempList.append("") # for icon
                fileurl = chapter_content_data.video
                if fileurl is not None and fileurl !="" :
                    path,ext = os.path.splitext(fileurl)
                    ext = ext.replace(".","").strip().lower()
                    if str(ext)== "mp4" or str(ext) == "pdf":
                        tempList.append(ext)
                    else:
                        tempList.append("")
                tempList.append(chapter_content_data.video)
                tempList.append(self.convert_utc_to_ist(chapter_content_data.created_at))
                tempList.append(self.convert_utc_to_ist(chapter_content_data.updated_at))

                data_str_list.append( tempList)
                tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter ]
        else:
            tempList = ["",""] + tempList + [section,sub_section,sub_sub_section]
            keyword = ""
            for _ in range(8):
                tempList.append("")
            # data_str_list.append( tempList )
            tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter ]


        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter ]
        
        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book,chapter ]

            for section_data in sections:
                sections_1=section_data.section
                if self.context['status'] == "approved":
                    sec_content = Content.objects.filter(section__id=section_data.id,approved=True).order_by("id")
                sub_section,sub_sub_section,content_name,file_url,text,keyword,keyword_list = "","","","","","",""
                section_keyword = SectionKeyword.objects.filter(section__id=section_data.id).order_by("id")
                if sec_content.exists():
                    for section_content_data in sec_content:
                        if  section_content_data.section_keywords.all().count() != 0:
                            linked_keyword = SectionKeyword.objects.filter(id__in=section_content_data.section_keywords.all())
                            keyword =','.join([str(x.keyword) for x in linked_keyword.all()])
                            
                        else:
                            keyword = ""
                        tempList = [section_content_data.content_name,"This resource is about "+str(chapters.book)+","+str(chapters.chapter)+"," +str(sections_1)] +tempList + [sections_1,sub_section,sub_sub_section]
                        tempList.append("Learn")
                        tempList.append(keyword)
                        tempList.append("Learner")
                        lastname=ContentContributors.objects.get(id=section_content_data.content_contributors_id).last_name
                        if lastname is None  :
                            lastname=""
                        tempList.append(str(ContentContributors.objects.get(id=section_content_data.content_contributors_id).first_name) + " "+ str(lastname)  )
                        tempList.append(ContentContributors.objects.get(id=section_content_data.content_contributors_id).school_name)
                        tempList.append("") # for icon
                        fileurl = section_content_data.video
                        if fileurl is not None and fileurl !="" :
                            path,ext = os.path.splitext(fileurl)
                            ext = ext.replace(".","").strip().lower()
                            if str(ext)== "mp4" or str(ext) == "pdf":
                                tempList.append(ext)
                            else:
                                tempList.append("")
                           
                        tempList.append(section_content_data.video)
                        tempList.append(self.convert_utc_to_ist(section_content_data.created_at))
                        tempList.append(self.convert_utc_to_ist(section_content_data.updated_at))
                        data_str_list.append( tempList )
                        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter]
                else:
                    tempList = ["", ""] + tempList + [sections_1,sub_section ,sub_sub_section]
                    keyword=""
                    for _ in range(8):
                        tempList.append("")
                    # data_str_list.append( tempList )
                    tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter ]

                tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter , section_data.section]

                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        sub_sections=sub_section_data.sub_section 
                        sub_sub_section,content_name,file_url,text,keyword,keyword_list = "","","","","",""
                        sub_section_keyword = SubSectionKeyword.objects.filter(sub_section__id=sub_section_data.id).order_by("id")
                        if self.context['status'] == "approved":
                            sub_sec_content = Content.objects.filter(sub_section__id=sub_section_data.id,approved=True).order_by("id")
                        if sub_sec_content.exists():

                            for sub_section_content_data in sub_sec_content:
                                if  sub_section_content_data.sub_section_keywords.all().count() != 0:
                                    linked_keyword = SubSectionKeyword.objects.filter(id__in=sub_section_content_data.sub_section_keywords.all())
                                    keyword =','.join([str(x.keyword) for x in linked_keyword.all()])
                                    
                                else:
                                    keyword = ""
                                tempList = [sub_section_content_data.content_name,"This resource is about "+str(chapters.book)+","+str(chapters.chapter)+","+ str(sections_1) +","+ str(sub_sections)]+tempList + [sub_sections,sub_sub_section ]
                                tempList.append("Learn")
                                tempList.append(keyword)
                                tempList.append("Learner")
                                lastname=ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).last_name
                                if lastname is None  :
                                    lastname=""
                                tempList.append(str(ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                tempList.append(ContentContributors.objects.get(id=sub_section_content_data.content_contributors_id).school_name)
                                tempList.append("") # for icon
                                fileurl = sub_section_content_data.video
                                if fileurl is not None and fileurl !="" :
                                    path,ext = os.path.splitext(fileurl)
                                    ext = ext.replace(".","").strip().lower()
                                    if str(ext)== "mp4" or str(ext) == "pdf":
                                        tempList.append(ext)
                                    else:
                                        tempList.append("")
                                else:
                                    tempList.append("")
                                
                                
                                tempList.append(sub_section_content_data.video)

                                tempList.append(self.convert_utc_to_ist(sub_section_content_data.created_at))
                                tempList.append(self.convert_utc_to_ist(sub_section_content_data.updated_at))
                                data_str_list.append( tempList )
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade,chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section ]
                        else:
                            tempList = ["",""]+tempList + [sub_sections,sub_sub_section]
                            keyword = ""
                            for _ in range(8):
                                tempList.append("")
                           
            
                            # data_str_list.append( tempList )
                            tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section ]

                        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section,sub_section_data.sub_section ]
         
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section in sub_sub_sections:
                                sub_sub_sections_1 = sub_sub_section.sub_sub_section 
                                content_name,file_url,text,keyword,keyword_list = "","","","",""
                                sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section__id=sub_sub_section.id).order_by("id")
                                if self.context['status'] == "approved":
                                    sub_sub_sec_content = Content.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True).order_by("id")
                                if sub_sub_sec_content.exists():

                                    for sub_sub_sec_content_data in sub_sub_sec_content:
                                        if  sub_sub_sec_content_data.sub_sub_section_keywords.all().count() != 0:
                                            linked_keyword = SubSubSectionKeyword.objects.filter(id__in=sub_sub_sec_content_data.sub_sub_section_keywords.all())
                                            keyword =','.join([str(x.keyword) for x in linked_keyword.all()])
                                            
                                        else:
                                            keyword = ""

                                        
                                        tempList = [sub_sub_sec_content_data.content_name,"This resource is about "+str(chapters.book)+","+str(chapters.chapter)+"," +str(sections_1) +","+ str(sub_sections) +","+str(sub_sub_sections_1)]+tempList + [sub_sub_sections_1]
                                        tempList.append("Learn")
                                        tempList.append(keyword)
                                        tempList.append("Learner")
                                        lastname=ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).last_name
                                        if lastname is None  :
                                            lastname=""
                                        tempList.append(str(ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                        tempList.append(ContentContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).school_name)
                                        tempList.append("") # for icon
                                        fileurl = sub_sub_sec_content_data.video
                                        if fileurl is not None and fileurl !="" :
                                            path,ext = os.path.splitext(fileurl)
                                            ext = ext.replace(".","").strip().lower()
                                            if str(ext)== "mp4" or str(ext) == "pdf":
                                                tempList.append(ext)
                                            else:
                                                tempList.append("")
                                        else:
                                            tempList.append("")
                                           
                                        tempList.append(sub_sub_sec_content_data.video)
                                        tempList.append(self.convert_utc_to_ist(sub_sub_sec_content_data.created_at))
                                        tempList.append(self.convert_utc_to_ist(sub_sub_sec_content_data.updated_at))
                                        data_str_list.append( tempList )
                                        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section,sub_section_data.sub_section ]

                                else:
                                    tempList = ["",""] + tempList + [sub_sub_sections_1]
                                    keyword = ""
                                    for _ in range(8):
                                        tempList.append("")
                                   
                                    # data_str_list.append( tempList )
                                    tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section,sub_section_data.sub_section ]
                                tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state,chapters.book.subject.grade, chapters.book.subject.grade.medium,  chapters.book.subject, chapters.book, chapter]

        for _i in data_str_list:
            print(len(_i))
        return data_str_list
        




class ContentStatusSerializerFileFormat(serializers.ModelSerializer):
    sas_token=serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ('id','video','sas_token')
    
    def get_sas_token(self,req):
        try:
            blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
            sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
            return sas_token
        except:
            return None


