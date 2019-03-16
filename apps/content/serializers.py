from rest_framework import routers, serializers
from .models import Content,ContentContributors
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword,SubSubSection
from apps.configuration.models import Book
from apps.hardspot.models import HardSpot
from apps.hardspot.serializers import HardSpotCreateSerializer
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
    def sub_sub_section(self,req):
        try:
            sub_sub_section_data = SubSubSection.objects.filter(sub_section=req.id)
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
            sub_section_data = SubSection.objects.filter(section=req.id)
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
            section_data = Section.objects.filter(chapter=req.id)
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
            chapter_data = Chapter.objects.filter(book=req.id)#.exclude(Q(book__hardspot_only=True) & ~Q(hardspot__isnull=False))
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
            sub_section_data = SubSubSection.objects.filter(subsection=req.id)
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
            sub_section_data = SubSection.objects.filter(section=req.id)
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
            section_data = Section.objects.filter(chapter=req.id)
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
            chapter_data = Chapter.objects.filter(book=req.id)
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
            import ipdb; ipdb.set_trace()
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
            return linked_keyword.keyword
        elif obj.sub_section_keywords.all().count() !=0:
            linked_keyword = SubSectionKeyword.objects.filter(id__in=obj.sub_section_keywords.all())
            return linked_keyword.keyword
        else:
            return None

class ApprovedContentSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
   
    class Meta:
        model = Chapter
       
        fields = ['chapter']

    

    def get_chapter(self, req):
        data_str_list = []
        chapters=Chapter.objects.filter(chapter=req.chapter).first()
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        chapter_content = Content.objects.filter(chapter__id=chapters.id,approved=True)
        section = ""
        sub_section = ""
        sub_sub_section=""
        tempList.append(section)
        tempList.append(sub_section)
        tempList.append(sub_sub_section)
        keyword = ""
        chapter_keyword = ChapterKeyword.objects.filter(chapter__id=chapters.id)
        for keys in chapter_keyword:
            keyword =  keyword + keys.keyword + ", "
        tempList.append(keyword)
        
        if chapter_content.exists():
            serializer = ContentDownloadSerializer(chapter_content, many=True)
            no_of_hardspot = len(serializer.data)
            if no_of_hardspot == 5:
                for data in serializer.data:
                    for key, value in data.items():
                        tempList.append(value)
            else:
                for data in serializer.data[:no_of_hardspot]:
                    for key, value in data.items():
                        tempList.append(value)
                for i in range(0,(5*(5-no_of_hardspot))):
                    tempList.append("")
            data_str_list.append( tempList )
        else:
            for x in range(0,25):
                tempList.append("")
            data_str_list.append( tempList )
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        sections=Section.objects.filter(chapter=req)
        if sections.exists():
            for section_data in sections:
                tempList.append(section_data.section)
                sec_content = Content.objects.filter(section__id=section_data.id,approved=True)
                sub_section = ""
                sub_sub_section = ""
                tempList.append(sub_section)
                tempList.append(sub_sub_section)
                keyword = ""
                section_keyword = SectionKeyword.objects.filter(section__id=section_data.id)
                for keys in section_keyword:
                    keyword = keyword + keys.keyword + ", "
                tempList.append(keyword)

                if sec_content.exists():
                    serializer = ContentDownloadSerializer(sec_content, many=True)

                    no_of_hardspot = len(serializer.data)
                    if no_of_hardspot == 5:
                        for data in serializer.data:
                            for key, value in data.items():
                                tempList.append(value)
                    else:
                        for data in serializer.data[:no_of_hardspot]:
                            for key, value in data.items():
                                tempList.append(value)
                        for i in range(0,(5*(5-no_of_hardspot))):
                            tempList.append("")
                    data_str_list.append( tempList )
                    
                else:
                    for x in range(0,25):
                        tempList.append("")
                    data_str_list.append( tempList )
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                
                sub_section=SubSection.objects.filter(section__id=section_data.id)
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        tempList.append( sub_section_data.sub_section )
                        sub_sub_section = ""
                        keyword = ""
                        tempList.append(sub_sub_section)

                        sub_section_keyword = SubSectionKeyword.objects.filter(sub_section__id=sub_section_data.id)
                        for keys in sub_section_keyword:
                            keyword = keyword + keys.keyword + ", "
                        tempList.append(keyword)

                        sub_sec_content = Content.objects.filter(sub_section__id=sub_section_data.id,approved=True)
                        if sub_sec_content.exists():
                            serializer = ContentDownloadSerializer(sub_sec_content, many=True)
                            no_of_hardspot = len(serializer.data)
                            if no_of_hardspot == 5:
                                for data in serializer.data:
                                    for key, value in data.items():
                                        tempList.append(value)
                            else:
                                for data in serializer.data[:no_of_hardspot]:
                                    for key, value in data.items():
                                        tempList.append(value)
                                for i in range(0,(5*(5-no_of_hardspot))):
                                    tempList.append("")
                            data_str_list.append( tempList )
                        else:
                            for x  in range(0,25):
                                tempList.append("")
                            data_str_list.append( tempList )
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id)
                        if sub_sub_sections.exists():
                            for sub_sub_section in sub_sub_sections:
                                tempList.append( sub_sub_section.sub_sub_section )
                                keyword = ""
                                sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section__id=sub_sub_section.id)
                                for keys in sub_sub_section_keyword:
                                    keyword = keyword + keys.keyword + ", "
                                tempList.append(keyword)

                                sub_sub_sec_content = Content.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True)
                                if sub_sub_sec_content.exists():
                                    serializer = ContentDownloadSerializer(sub_sub_sec_content, many=True)
                                    no_of_hardspot = len(serializer.data)
                                    if no_of_hardspot == 5:
                                        for data in serializer.data:
                                            for key, value in data.items():
                                                tempList.append(value)
                                    else:
                                        for data in serializer.data[:no_of_hardspot]:
                                            for key, value in data.items():
                                                tempList.append(value)
                                        for i in range(0,(5*(5-no_of_hardspot))):
                                            tempList.append("")
                                    data_str_list.append( tempList )
                                else:
                                    for x  in range(0,25):
                                        tempList.append("")
                                    data_str_list.append( tempList )

                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
        for i in data_str_list:
            print(i)
            print(len(i))
        return data_str_list
    
class ContentStatusSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
    class Meta:
        model = Chapter
        fields = ['chapter']
    
    def get_chapter(self, req):
        data_str_list = []
        chapters=Chapter.objects.filter(chapter=req.chapter).first()
        sections=Section.objects.filter(chapter=req)
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        if sections.exists():
            for section_data in sections:
                sub_section=SubSection.objects.filter(section__id=section_data.id)
                tempList.append( section_data.section )
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        tempList.append( sub_section_data.sub_section )
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
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                else:
                    sub_section = " "
                    tempList.append(sub_section)
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
                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        else:
            section = " "
            sub_section = " "
            
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
            data_str_list.append( tempList )

        return data_str_list

class ContentContributorsSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    textbook_name=serializers.SerializerMethodField()
    class Meta:
        model = Content
        fields = ['first_name',
                'last_name',
                'mobile',
                'email',
                'textbook_name']
    def get_first_name(self, obj):
        first_name=ContentContributors.objects.filter(id=obj.content_contributors.id).first().first_name
        return first_name
    def get_last_name(self, obj):
        last_name=ContentContributors.objects.filter(id=obj.content_contributors.id).first().last_name
        return last_name
    def get_mobile(self, obj):
        mobile=ContentContributors.objects.filter(id=obj.content_contributors.id).first().mobile
        return mobile
    def get_email(self, obj):
        email=ContentContributors.objects.filter(id=obj.content_contributors.id).first().email
        return email
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
        else:
            return None