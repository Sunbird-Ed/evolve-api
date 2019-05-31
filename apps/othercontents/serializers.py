from rest_framework import routers, serializers
from .models import OtherContributors,OtherContent,SchoolName
from apps.dataupload.models import (Chapter,
    Section,
    SubSection,
    ChapterKeyword,
    SectionKeyword,
    SubSectionKeyword,
    SubSubSection,
    SubSubSectionKeyword,
    SubSubSection,)
from apps.hardspot.models import HardSpot
from apps.content.models import Content
from apps.configuration.models import Book,Grade,Subject
from apps.hardspot.models import HardSpot
from datetime import datetime, timedelta
import os,ntpath
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
)
from evolve import settings
accountName = settings.AZURE_ACCOUNT_NAME
accountKey = settings.AZURE_ACCOUNT_KEY
containerName= settings.AZURE_CONTAINER

class OtherContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model=OtherContributors
        fields='__all__'

class SchoolNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolName
        fields='__all__'


class OtherContentListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=OtherContent
        fields='__all__'


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
            contributions_approved=OtherContent.objects.filter(sub_sub_section_id=req.id,approved=True,tags__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=OtherContent.objects.filter(sub_sub_section_id=req.id,approved=False,approved_by=None,tags__id = self.context.get('tagname', None)).count()
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
            contributions_approved=OtherContent.objects.filter(sub_section_id=req.id,approved=True,tags__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=OtherContent.objects.filter(sub_section_id=req.id,approved=False,approved_by=None,tags__id = self.context.get('tagname', None)).count()
            return (contributions_approved + contributions_pending)
        except:
            return None
    def get_sub_sub_section(self,req):
        try:
            sub_sub_section_data = SubSubSection.objects.filter(subsection=req.id).order_by('id')
            serializer = SubSubSectionSerializer(sub_sub_section_data, many=True,context=self.context)
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
            serializer = SubSectionSerializer(sub_section_data, many=True,context=self.context)
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
            contributions_approved=OtherContent.objects.filter(section_id=req.id,approved =True,tags__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=OtherContent.objects.filter(section_id=req.id,approved=False,approved_by=None,tags__id = self.context.get('tagname', None)).count()
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
            contributions_approved=OtherContent.objects.filter(chapter_id=req.id,approved=True,tags__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=OtherContent.objects.filter(chapter_id=req.id,approved=False,approved_by=None,tags__id = self.context.get('tagname', None)).count()
            return (contributions_approved + contributions_pending)
        except:
            return None       

    def get_section(self, req):
        try:
            section_data = Section.objects.filter(chapter=req.id).order_by('id')
            serializer = SectionNestedSerializer(section_data, many=True,context=self.context)
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
            # import ipdb;ipdb.set_trace()

            chapter_data = Chapter.objects.filter(book=req.id).order_by('id')
            serializer = ChapterNestedSerializer(chapter_data, many=True, context=self.context)
            data = serializer.data
            return data
        except:
            return None


# <-------------------------------------------------other content review--------------------------------------------------------------------->



class OtherContentSubSubSectionSerializer(serializers.ModelSerializer):
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
            if self.context['school_name'] != "0":
                count = OtherContent.objects.filter(sub_sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                count = OtherContent.objects.filter(sub_sub_section=req.id,tags__id = self.context['tag_code']).count()
            return count
        except:
            return None

    def get_approved(self, req):
        try:
            if self.context['school_name'] != "0":
                sub_sec_approved = OtherContent.objects.filter(approved=True,sub_sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                sub_sec_approved = OtherContent.objects.filter(approved=True,sub_sub_section=req.id,tags__id = self.context['tag_code']).count()

            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            if  self.context['school_name'] != "0":
                sub_sec_reject = OtherContent.objects.filter(approved=False,sub_sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).exclude(approved_by=None).count()
            else:
                sub_sec_reject = OtherContent.objects.filter(approved=False,sub_sub_section=req.id,tags__id = self.context['tag_code']).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            if  self.context['school_name'] != "0":
                sub_sec_pending = OtherContent.objects.filter(approved=False,sub_sub_section=req.id,approved_by=None,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                sub_sec_pending = OtherContent.objects.filter(approved=False,sub_sub_section=req.id,approved_by=None,tags__id = self.context['tag_code']).count()
            return sub_sec_pending
        except:
            return None



class OtherContentSubSectionSerializer(serializers.ModelSerializer):
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
            serializer = OtherContentSubSubSectionSerializer(sub_section_data, many=True,context= self.context)
            data = serializer.data
            return data
        except:
            return None

    
    def get_total(self, req):
        try:
            if self.context['school_name'] != "0":
                count = OtherContent.objects.filter(sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                count = OtherContent.objects.filter(sub_section=req.id,tags__id = self.context['tag_code']).count()

            return count
        except:
            return None

    def get_approved(self, req):
        try:
            if self.context['school_name'] != "0":
                sub_sec_approved = OtherContent.objects.filter(approved=True,sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                sub_sec_approved = OtherContent.objects.filter(approved=True,sub_section=req.id,tags__id = self.context['tag_code']).count()
            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            if self.context['school_name'] != "0":
                sub_sec_reject = OtherContent.objects.filter(approved=False,sub_section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).exclude(approved_by=None).count()
            else:
                sub_sec_reject = OtherContent.objects.filter(approved=False,sub_section=req.id,tags__id = self.context['tag_code']).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            if  self.context['school_name'] != "0":
                sub_sec_pending = OtherContent.objects.filter(approved=False,sub_section=req.id,approved_by=None,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                sub_sec_pending = OtherContent.objects.filter(approved=False,sub_section=req.id,approved_by=None,tags__id = self.context['tag_code']).count()

            return sub_sec_pending
        except:
            return None



class OtherContentSectionNestedSerializer(serializers.ModelSerializer):
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
            serializer = OtherContentSubSectionSerializer(sub_section_data, many=True,context= self.context)
            data = serializer.data
            return data
        except:
            return None
    def get_total(self, req):
        try:
            if self.context['school_name'] != "0":
                count = OtherContent.objects.filter(section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                count = OtherContent.objects.filter(section=req.id,tags__id = self.context['tag_code']).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            if self.context['school_name'] != "0":
                sec_approved = OtherContent.objects.filter(approved=True,section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            
            else:
                sec_approved = OtherContent.objects.filter(approved=True,section=req.id,tags__id = self.context['tag_code']).count()
            return sec_approved
        except:
            return None
    def get_reject(self, req):
        try:
            if  self.context['school_name'] != "0":
                sec_reject = OtherContent.objects.filter(approved=False,section=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).exclude(approved_by=None).count()
            else:
                sec_reject = OtherContent.objects.filter(approved=False,section=req.id,tags__id = self.context['tag_code']).exclude(approved_by=None).count()
            return sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            if  self.context['school_name'] != "0":
                sec_pending = OtherContent.objects.filter(approved=False,section=req.id,approved_by=None,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                sec_pending = OtherContent.objects.filter(approved=False,section=req.id,approved_by=None,tags__id = self.context['tag_code'],).count()
            return sec_pending
        except:
            return None



class OtherContentChapterNestedSerializer(serializers.ModelSerializer):
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
            serializer = OtherContentSectionNestedSerializer(section_data, many=True,context= self.context)
            data = serializer.data
            return data
        except:
            return None

    def get_total(self, req):
        try:
            if  self.context['school_name'] != "0":
                count = OtherContent.objects.filter(chapter=req.id, tags__id= self.context['tag_code'], content_contributors__school_name__id=self.context['school_name'] ).count()
            else:
                count = OtherContent.objects.filter(chapter=req.id, tags__id= self.context['tag_code'] ).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            if  self.context['school_name'] != "0":
                chapter_approved = OtherContent.objects.filter(approved=True,chapter=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                chapter_approved = OtherContent.objects.filter(approved=True,chapter=req.id,tags__id = self.context['tag_code']).count()
            return chapter_approved
        except:
            return None
    def get_reject(self, req):
        try:
            if  self.context['school_name'] != "0":
                chapter_reject = OtherContent.objects.filter(approved=False,chapter=req.id,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name'] ).exclude(approved_by=None).count()
            else:
                chapter_reject = OtherContent.objects.filter(approved=False,chapter=req.id,tags__id = self.context['tag_code'] ).exclude(approved_by=None).count()
            return chapter_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            if  self.context['school_name'] != "0":
                chapter_pending = OtherContent.objects.filter(approved=False,chapter=req.id,approved_by=None,tags__id = self.context['tag_code'],content_contributors__school_name__id=self.context['school_name']).count()
            else:
                chapter_pending = OtherContent.objects.filter(approved=False,chapter=req.id,approved_by=None,tags__id = self.context['tag_code']).count()
            return chapter_pending
        except:
            return None

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

class OtherContentContributorSerializer(serializers.ModelSerializer):
    school_name = serializers.SerializerMethodField()
    class Meta:
        model = OtherContributors
        fields='__all__'

    def get_school_name(self,req):
        school_name=SchoolName.objects.filter(id=req.school_name.id ).first().school_name
        return school_name         



class OtherContentBookListSerializer(serializers.ModelSerializer):
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
            serializer = OtherContentChapterNestedSerializer(chapter_data, many=True, context= self.context)
            data = serializer.data
            return data
        except:
            return None



class OtherContentStatusSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField()
    sas_token=serializers.SerializerMethodField()
    content_contributors = serializers.SerializerMethodField()
    
    class Meta:
        model = OtherContent
        fields = ('id','chapter','section','sub_section','sub_sub_section','content_name','keywords','file_url','text','approved','approved_by','comment', 'content_contributors','sas_token')
    
    def get_sas_token(self,req):
        try:
            # import ipdb;ipdb.set_trace()
            blobService = BlockBlobService(account_name=accountName, account_key=accountKey)
            sas_token = blobService.generate_container_shared_access_signature(containerName,ContainerPermissions.READ, datetime.utcnow() + timedelta(hours=1))
            return sas_token
        except:
            return None

    def get_content_contributors(self, req):
        try:
            content_contributor = OtherContributors.objects.filter(id=req.content_contributors.id).first()
            serializer = OtherContentContributorSerializer(content_contributor)
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
                # import ipdb;ipdb.set_trace()
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

    def update(self, instance, validated_data):
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by=self.context.get('user', None)
        # instance.rating = self.validated_data.get('rating', instance.rating)
        # instance.rated_by = self.context.get('user', None)
        instance.comment = self.validated_data.get('comment', None)
        instance.save()
        return instance



class OtherContentDetailListSerializer(serializers.ModelSerializer):
    # total_hardspot=serializers.SerializerMethodField()
    # approved_hardspot=serializers.SerializerMethodField()
    total_content=serializers.SerializerMethodField()
    approved_content=serializers.SerializerMethodField()
    rejected_content = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = '__all__'
        depth=3


    def get_total_content(self,req):
        tag=self.context['code_name']
        chapter_count=OtherContent.objects.filter(chapter__book__id=req.id,tags__id = tag).count()
        section_count=OtherContent.objects.filter(section__chapter__book__id=req.id,tags__id = tag).count()
        subsection_count=OtherContent.objects.filter(sub_section__section__chapter__book__id=req.id,tags__id = tag).count()
        subsubsection_count=OtherContent.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,tags__id = tag).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)
        

    def get_approved_content(self,req):

        tag=self.context['code_name']
        chapter_count=OtherContent.objects.filter(chapter__book__id=req.id,approved=True,tags__id = tag).count()
        section_count=OtherContent.objects.filter(section__chapter__book__id=req.id,approved=True,tags__id = tag).count()
        subsection_count=OtherContent.objects.filter(sub_section__section__chapter__book__id=req.id,approved=True,tags__id = tag).count()
        subsubsection_count=OtherContent.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=True,tags__id = tag).count()
        return(chapter_count + section_count + subsection_count + subsubsection_count)

    def get_rejected_content(self,req):

        tag=self.context['code_name']
        chapter_count=OtherContent.objects.filter(chapter__book__id=req.id,approved=False,tags__id = tag).exclude(approved_by=None).count()
        section_count=OtherContent.objects.filter(section__chapter__book__id=req.id,approved=False,tags__id = tag).exclude(approved_by=None).count()
        subsection_count=OtherContent.objects.filter(sub_section__section__chapter__book__id=req.id,approved=False,tags__id = tag).exclude(approved_by=None).count()
        subsubsection_count=OtherContent.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=False,tags__id = tag).exclude(approved_by=None).count()
        
        return(chapter_count + section_count + subsection_count + subsubsection_count)




class OtherContentContributorsSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    # city_name=serializers.SerializerMethodField()
    school_name=serializers.SerializerMethodField()
    textbook_name=serializers.SerializerMethodField()
    grade=serializers.SerializerMethodField()
    subject=serializers.SerializerMethodField()
    class Meta:
        model = OtherContent
        fields = ['first_name',
                'last_name',
                'mobile',
                'email',
                'school_name',
                'textbook_name',
                'grade',
                'subject']

    def get_first_name(self, obj):
        try:
            first_name=OtherContributors.objects.filter(id=obj.content_contributors.id).first().first_name
            return first_name
        except Exception as e:
            return None 

    def get_last_name(self, obj):

        try:
            last_name=OtherContributors.objects.filter(id=obj.content_contributors.id).first().last_name
            return last_name
        except Exception as e:
            return None
        
    def get_mobile(self, obj):
        try:
            mobile=OtherContributors.objects.filter(id=obj.content_contributors.id).first().mobile
            return mobile
        except Exception as e:
            return None
       
    def get_email(self, obj):

        try:
            email=OtherContributors.objects.filter(id=obj.content_contributors.id).first().email
            return email
        except Exception as e:
            return None
        

    def get_school_name(self ,obj):
        try:
            school_name=SchoolName.objects.filter(id=obj.content_contributors.school_name.id).first().school_name         
            return school_name
        except Exception as e:
            None
        
  
    def get_textbook_name(self, obj):
        try:
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
        except Exception as e:
            return None

    def get_grade(self, obj):
        try:
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
        except Exception as e:
            return None
        

    def get_subject(self, obj):
        
        try:
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
        except Exception as e:
            return None
       


class OtherContentDownloadSerializer(serializers.ModelSerializer):
    selected_keyword = serializers.SerializerMethodField()
    class Meta:
        model=OtherContent
        fields=('content_name','file_url','text','selected_keyword')

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



class ApprovedOtherContentSerializer(serializers.ModelSerializer):
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
            chapter_content = OtherContent.objects.filter(chapter__id=chapters.id,approved=True,tags__id=self.context['tag_id']).order_by("id")
        elif self.context['status'] == "rejected":
            chapter_content = OtherContent.objects.filter(chapter__id=chapters.id,approved=False,tags__id=self.context['tag_id']).exclude(approved_by=None).order_by("id")
        section, sub_section, sub_sub_section, content_name,file_url, text, keyword, keyword_list = "","","","","","","",""
        chapter_keyword = ChapterKeyword.objects.filter(chapter__id=chapters.id).order_by("id")
        if chapter_content.exists():

            for chapter_content_data in chapter_content:
                # import ipdb;ipdb.set_trace()
                if  chapter_content_data.chapter_keywords.all().count() != 0:
                    linked_keyword = ChapterKeyword.objects.filter(id__in=chapter_content_data.chapter_keywords.all())
                    keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                    
                else:
                    keyword_list = ""
                
               
                keyword=self.getkeywords(chapter_keyword)
                tempList = tempList + [section,sub_section,sub_sub_section,keyword,chapter_content_data.content_name,chapter_content_data.file_url,chapter_content_data.text]
                keyword = ""
                lastname=OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).last_name
                if lastname is None  :
                    lastname=""
                tempList.append(str(OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).first_name) + " "+ lastname  )
                tempList.append(OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).school_name.school_name) 
                if self.context['tag_id'] == "9" or self.context['tag_id'] == "10" or self.context['tag_id'] == "11":
                    fileurl = chapter_content_data.file_url
                    if fileurl is not None and fileurl !="" :
                        path,ext = os.path.splitext(fileurl)
                        ext = ext.replace(".","").strip().lower()
                        if str(ext)== "mp4" or str(ext) == "pdf":
                            tempList.append(ext)
                        else:
                            tempList.append("")
                    else:
                        tempList.append("Text")
                else:
                    tempList.append("Text")
                
                if self.context['status'] == "rejected":
                    tempList.append(chapter_content_data.comment)
                tempList.append(keyword_list)
                data_str_list.append( tempList)
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        else:
            keyword=self.getkeywords(chapter_keyword)
            tempList = tempList + [section,sub_section,sub_sub_section,keyword]
            keyword = ""
            for _ in range(7):
                tempList.append("")
            if self.context['status'] == "rejected":
                tempList.append("")
            data_str_list.append( tempList )
            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]


        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        
        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, ]

            for section_data in sections:
                sections_1=section_data.section
                if self.context['status'] == "approved":
                    sec_content = OtherContent.objects.filter(section__id=section_data.id,approved=True,tags__id=self.context['tag_id']).order_by("id")
                elif self.context['status'] == "rejected":
                    sec_content = OtherContent.objects.filter(section__id=section_data.id,approved=False,tags__id=self.context['tag_id']).exclude(approved_by=None).order_by("id")
                sub_section,sub_sub_section,content_name,file_url,text,keyword,keyword_list = "","","","","","",""
                section_keyword = SectionKeyword.objects.filter(section__id=section_data.id).order_by("id")
                if sec_content.exists():
                    for section_content_data in sec_content:
                        keyword=self.getkeywords(section_keyword)
                        if  section_content_data.section_keywords.all().count() != 0:
                            linked_keyword = SectionKeyword.objects.filter(id__in=section_content_data.section_keywords.all())
                            keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                            
                        else:
                            keyword_list = ""
                        tempList = tempList + [sections_1,sub_section,sub_sub_section,keyword,section_content_data.content_name,section_content_data.file_url,section_content_data.text]
                        keyword=""
                        lastname=OtherContributors.objects.get(id=section_content_data.content_contributors_id).last_name
                        if lastname is None  :
                            lastname=""
                        tempList.append(str(OtherContributors.objects.get(id=section_content_data.content_contributors_id).first_name) + " "+ str(lastname)  )
                        tempList.append(OtherContributors.objects.get(id=section_content_data.content_contributors_id).school_name.school_name)
                        if self.context['tag_id'] == "9" or self.context['tag_id'] == "10" or self.context['tag_id'] == "11":
                            fileurl = section_content_data.file_url
                            if fileurl is not None and fileurl !="" :
                                path,ext = os.path.splitext(fileurl)
                                ext = ext.replace(".","").strip().lower()
                                if str(ext)== "mp4" or str(ext) == "pdf":
                                    tempList.append(ext)
                                else:
                                    tempList.append("")
                            else:
                                tempList.append("Text")
                        else:
                            tempList.append("Text")
                        tempList.append(keyword_list)
                        if self.context['status'] == "rejected":
                            tempList.append(section_content_data.comment)
                        data_str_list.append( tempList )
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, ]
                else:
                    keyword = self.getkeywords(section_keyword)
                    tempList = tempList + [sections_1,sub_section ,sub_sub_section,keyword]
                    keyword=""
                    for _ in range(7):
                        tempList.append("")
                    if self.context['status'] == "rejected":
                        tempList.append("")
      
                    data_str_list.append( tempList )
                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]

                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter , section_data.section]

                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        sub_sections=sub_section_data.sub_section 
                        sub_sub_section,content_name,file_url,text,keyword,keyword_list = "","","","","",""
                        sub_section_keyword = SubSectionKeyword.objects.filter(sub_section__id=sub_section_data.id).order_by("id")
                        if self.context['status'] == "approved":
                            sub_sec_content = OtherContent.objects.filter(sub_section__id=sub_section_data.id,approved=True,tags__id=self.context['tag_id']).order_by("id")
                        elif self.context['status'] == "rejected":
                            sub_sec_content = OtherContent.objects.filter(sub_section__id=sub_section_data.id,approved=False,tags__id=self.context['tag_id']).exclude(approved_by=None).order_by("id")
                        if sub_sec_content.exists():
                            for sub_section_content_data in sub_sec_content:
                                keyword = self.getkeywords(sub_section_keyword)
                                if  sub_section_content_data.sub_section_keywords.all().count() != 0:
                                    linked_keyword = SubSectionKeyword.objects.filter(id__in=sub_section_content_data.sub_section_keywords.all())
                                    keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                                    
                                else:
                                    keyword_list = ""
                                # if (sub_section_content_data.text != ""  or sub_section_content_data.text !=  None ) and (sub_section_content_data.file_url == None or sub_section_content_data.file_url == ""):
                                #     text= ""
                                # else: 
                                #     text = "Text"
                                tempList = tempList + [sub_sections,sub_sub_section,keyword,sub_section_content_data.content_name,sub_section_content_data.file_url,sub_section_content_data.text]
                                keyword = ""
                                lastname=OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).last_name
                                if lastname is None  :
                                    lastname=""
                                tempList.append(str(OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                tempList.append(OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).school_name.school_name)
                                if self.context['tag_id'] == "9" or self.context['tag_id'] == "10" or self.context['tag_id'] == "11":
                                    fileurl = sub_section_content_data.file_url
                                    if fileurl is not None and fileurl !="" :
                                        path,ext = os.path.splitext(fileurl)
                                        ext = ext.replace(".","").strip().lower()
                                        if str(ext)== "mp4" or str(ext) == "pdf":
                                            tempList.append(ext)
                                        else:
                                            tempList.append("")
                                    else:
                                        tempList.append("Text")
                                else:
                                    tempList.append("Text")
                                
                                if self.context['status'] == "rejected":
                                    tempList.append(sub_section_content_data.comment)
                                tempList.append(keyword_list)
                                data_str_list.append( tempList )
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                        else:
                            keyword = self.getkeywords(sub_section_keyword)
                            tempList = tempList + [sub_sections,sub_sub_section,keyword]
                            keyword = ""
                            for _ in range(7):
                                tempList.append("")
                            if self.context['status'] == "rejected":
                                    tempList.append("")
            
                            data_str_list.append( tempList )
                            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]

                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
         
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section in sub_sub_sections:
                                sub_sub_sections_1 = sub_sub_section.sub_sub_section 
                                content_name,file_url,text,keyword,keyword_list = "","","","",""
                                sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section__id=sub_sub_section.id).order_by("id")
                                if self.context['status'] == "approved":
                                    sub_sub_sec_content = OtherContent.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True,tags__id=self.context['tag_id']).order_by("id")
                                elif self.context['status'] == "rejected":
                                    sub_sub_sec_content = OtherContent.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=False,tags__id=self.context['tag_id']).exclude(approved_by=None).order_by("id")


                                if sub_sub_sec_content.exists():

                                    for sub_sub_sec_content_data in sub_sub_sec_content:
                                        keyword = self.getkeywords(sub_sub_section_keyword)
                                        # keyword = self.getkeywords(sub_section_keyword)
                                        if  sub_sub_sec_content_data.sub_sub_section_keywords.all().count() != 0:
                                            linked_keyword = SubSubSectionKeyword.objects.filter(id__in=sub_sub_sec_content_data.sub_sub_section_keywords.all())
                                            keyword_list =','.join([str(x.keyword) for x in linked_keyword.all()])
                                            
                                        else:
                                            keyword_list = ""
                                        # if (sub_sub_sec_content_data.text != ""  or sub_sub_sec_content_data.text !=  None ) and (sub_sub_sec_content_data.file_url == None or sub_sub_sec_content_data.file_url == ""):
                                        #     text= ""
                                        # else: 
                                        #     text = "Text"
                                        tempList = tempList + [sub_sub_sections_1,keyword,sub_sub_sec_content_data.content_name,sub_sub_sec_content_data.file_url,sub_sub_sec_content_data.text]
                                        keyword = ""
                                        lastname=OtherContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).last_name
                                        if lastname is None  :
                                            lastname=""
                                        tempList.append(str(OtherContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).first_name) + " "+ lastname  )
                                        tempList.append(OtherContributors.objects.get(id=sub_sub_sec_content_data.content_contributors_id).school_name.school_name)
                                        if self.context['tag_id'] == "9" or self.context['tag_id'] == "10" or self.context['tag_id'] == "11":
                                            fileurl = sub_sub_sec_content_data.file_url
                                            if fileurl is not None and fileurl !="" :
                                                path,ext = os.path.splitext(fileurl)
                                                ext = ext.replace(".","").strip().lower()
                                                if str(ext)== "mp4" or str(ext) == "pdf":
                                                    tempList.append(ext)
                                                else:
                                                    tempList.append("")
                                            else:
                                                tempList.append("Text")
                                        else:
                                            tempList.append("Text")
                                        if self.context['status'] == "rejected":
                                            tempList.append(sub_sub_sec_content_data.comment)
                                        tempList.append(keyword_list)
                                        data_str_list.append( tempList )
                                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]

                                else:
                                    keyword = self.getkeywords(sub_sub_section_keyword)
                                    tempList = tempList + [sub_sub_sections_1,keyword]
                                    keyword = ""
                                    for _ in range(7):
                                        tempList.append("")
                                    if self.context['status'] == "rejected":
                                        tempList.append("")
                                    data_str_list.append( tempList )
                                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
        



        for _i in data_str_list:
            print(len(_i))
            # print("sdfsf: >>" +str(_i))
        return data_str_list

        

class HardSpotDetailListSerializer(serializers.ModelSerializer):
    total_content=serializers.SerializerMethodField()
    approved_content=serializers.SerializerMethodField()
    rejected_content=serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        depth=3

    def get_total_content(self,req):
        chapter_count=HardSpot.objects.filter(chapter__book__id=req.id).count()
        section_count=HardSpot.objects.filter(section__chapter__book__id=req.id).count()
        subsection_count=HardSpot.objects.filter(sub_section__section__chapter__book__id=req.id).count()
        subsubsection_count=HardSpot.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)

    def get_approved_content(self,req):
        chapter_count=HardSpot.objects.filter(chapter__book__id=req.id,approved=True).count()
        section_count=HardSpot.objects.filter(section__chapter__book__id=req.id,approved=True).count()
        subsection_count=HardSpot.objects.filter(sub_section__section__chapter__book__id=req.id,approved=True).count()
        subsubsection_count=HardSpot.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=True).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)

    def get_rejected_content(self,req):
        chapter_count=HardSpot.objects.filter(chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        section_count=HardSpot.objects.filter(section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        subsection_count=HardSpot.objects.filter(sub_section__section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        subsubsection_count=HardSpot.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        return(chapter_count + section_count + subsection_count + subsubsection_count)





class ContentDetailListSerializer(serializers.ModelSerializer):
    total_content=serializers.SerializerMethodField()
    approved_content=serializers.SerializerMethodField()
    rejected_content = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = '__all__'
        depth=3

   

    def get_total_content(self,req):
        chapter_count=Content.objects.filter(chapter__book__id=req.id).count()
        section_count=Content.objects.filter(section__chapter__book__id=req.id).count()
        subsection_count=Content.objects.filter(sub_section__section__chapter__book__id=req.id).count()
        subsubsection_count=Content.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)
        

    def get_approved_content(self,req):
        chapter_count=Content.objects.filter(chapter__book__id=req.id,approved=True).count()
        section_count=Content.objects.filter(section__chapter__book__id=req.id,approved=True).count()
        subsection_count=Content.objects.filter(sub_section__section__chapter__book__id=req.id,approved=True).count()
        subsubsection_count=Content.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=True).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)

    def get_rejected_content(self,req):
        chapter_count=Content.objects.filter(chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        section_count=Content.objects.filter(section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        subsection_count=Content.objects.filter(sub_section__section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()
        subsubsection_count=Content.objects.filter(sub_sub_section__subsection__section__chapter__book__id=req.id,approved=False).exclude(approved_by=None).count()

        return(chapter_count + section_count + subsection_count + subsubsection_count)




class OtherContentStatusSerializer(serializers.ModelSerializer):
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
       
        chapter_con = OtherContent.objects.filter(chapter__id=chapters.id,tags__id=self.context['tag_id'])
        section, sub_section, sub_sub_section, content_name,file_url, text, keyword, keyword_list = "","","","","","","",""
        # import ipdb;ipdb.set_trace()
        if chapter_con.exists():
            for chapter_content_data in chapter_con:
                tempList.append(section)
                tempList.append(sub_section)
                tempList.append(sub_sub_section)
                tempList.append(chapter_content_data.content_name)
                tempList.append(OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).school_name.school_name) 
                tempList.append(OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).mobile) 
                tempList.append(OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).email) 
                filename = chapter_content_data.file_url
                if filename is not None:
                    head, tail = ntpath.split(filename)
                    if tail is not None or tail !="":
                        tempList.append(tail)
                    else:
                        tempList.append("")
                else:
                    tempList.append("")
                approved = chapter_content_data.approved
                approved_by = chapter_content_data.approved_by
                if approved_by is not None and  approved is True:
                    tempList.append("approved")
                elif approved_by is not None and  approved is False:
                    tempList.append("rejected")
                elif approved_by is  None and  approved is False:
                    tempList.append("pending")
                else:
                    tempList.append("")
                tag_id=OtherContributors.objects.get(id=chapter_content_data.content_contributors_id).tags.id
                if tag_id == "7":
                    tempList.append("lod")
                elif tag_id == "11":
                    tempList.append("lp")
                elif tag_id == "10":
                    tempList.append("expr")
                elif tag_id == "9":
                    tempList.append("expl")
                elif tag_id == "8":
                    tempList.append("cq")
                else:
                    tempList.append("")

                data_str_list.append( tempList)
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]

        else:
            for i in range(10):
                tempList.append("")
            data_str_list.append( tempList)
            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]


        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]

        
        # data_str_list.append( tempList)
        # print("1:>>"+str(len(tempList)))
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            for section_data in sections:
                section_con = OtherContent.objects.filter(section__id=section_data.id,tags__id=self.context['tag_id'])
                if section_con.exists():
                    for section_content_data in section_con:
                        tempList.append( section_data.section )
                        tempList.append("")
                        tempList.append("")
                        tempList.append(section_content_data.content_name)
                        tempList.append(OtherContributors.objects.get(id=section_content_data.content_contributors_id).school_name.school_name) 
                        tempList.append(OtherContributors.objects.get(id=section_content_data.content_contributors_id).mobile) 
                        tempList.append(OtherContributors.objects.get(id=section_content_data.content_contributors_id).email) 
                        filename = section_content_data.file_url
                        if filename is not None:
                            head, tail = ntpath.split(filename)
                            if tail is not None or tail !="":
                                tempList.append(tail)
                            else:
                                tempList.append("")
                        else:
                            tempList.append("")
                        approved = section_content_data.approved
                        approved_by = section_content_data.approved_by
                        if approved_by is not None and  approved is True:
                            tempList.append("approved")
                        elif approved_by is not None and  approved is False:
                            tempList.append("rejected")
                        elif approved_by is  None and  approved is False:
                            tempList.append("pending")
                        else:
                            tempList.append("")
                        tag_id=OtherContributors.objects.get(id=section_content_data.content_contributors_id).tags.id
                        if tag_id == "7":
                            tempList.append("lod")
                        elif tag_id == "11":
                            tempList.append("lp")
                        elif tag_id == "10":
                            tempList.append("expr")
                        elif tag_id == "9":
                            tempList.append("expl")
                        elif tag_id == "8":
                            tempList.append("cq")
                        else:
                            tempList.append("")
                        data_str_list.append( tempList)
                        # print("2:>>"+str(len(tempList)))

                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
                else:
                    tempList.append( section_data.section )
                    for i in range(9):
                        tempList.append("")
                    data_str_list.append(tempList)
                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]


                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        sub_section_con = OtherContent.objects.filter(sub_section__id=sub_section_data.id,tags__id=self.context['tag_id'])
                        if sub_section_con.exists():
                            for sub_section_content_data in sub_section_con:
                                tempList.append( sub_section_data.sub_section )
                                tempList.append("")
                                tempList.append(sub_section_content_data.content_name)
                                tempList.append(OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).school_name.school_name) 
                                tempList.append(OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).mobile) 
                                tempList.append(OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).email) 
                                filename = sub_section_content_data.file_url
                                if filename is not None:
                                    head, tail = ntpath.split(filename)
                                    if tail is not None or tail !="":
                                        tempList.append(tail)
                                    else:
                                        tempList.append("")
                                else:
                                    tempList.append("")
                                approved = sub_section_content_data.approved
                                approved_by = sub_section_content_data.approved_by
                                if approved_by is not None and  approved is True:
                                    tempList.append("approved")
                                elif approved_by is not None and  approved is False:
                                    tempList.append("rejected")
                                elif approved_by is  None and  approved is False:
                                    tempList.append("pending")
                                else:
                                    tempList.append("")

                                tag_id=OtherContributors.objects.get(id=sub_section_content_data.content_contributors_id).tags.id
                                if tag_id == "7":
                                    tempList.append("lod")
                                elif tag_id == "11":
                                    tempList.append("lp")
                                elif tag_id == "10":
                                    tempList.append("expr")
                                elif tag_id == "9":
                                    tempList.append("expl")
                                elif tag_id == "8":
                                    tempList.append("cq")
                                else:
                                    tempList.append("")
                                data_str_list.append( tempList)
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                        else:
                            tempList.append( sub_section_data.sub_section )
                            for i in range(8):
                                tempList.append("")
                            data_str_list.append( tempList)
                            tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]

                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section_data in sub_sub_sections:
                                sub_sub_section_con = OtherContent.objects.filter(sub_sub_section__id=sub_sub_section_data.id,tags__id=self.context['tag_id'])
                                if sub_sub_section_con.exists():
                                    for sub_sub_section_con_data in sub_sub_section_con:
                                        tempList.append(sub_sub_section_data.sub_sub_section)
                                        tempList.append(sub_sub_section_con_data.content_name)
                                        tempList.append(OtherContributors.objects.get(id=sub_sub_section_con_data.content_contributors_id).school_name.school_name) 
                                        tempList.append(OtherContributors.objects.get(id=sub_sub_section_con_data.content_contributors_id).mobile) 
                                        tempList.append(OtherContributors.objects.get(id=sub_sub_section_con_data.content_contributors_id).email) 
                                        filename = sub_sub_section_con_data.file_url
                                        if filename is not None:
                                            head, tail = ntpath.split(filename)
                                            if tail is not None or tail !="":
                                                tempList.append(tail)
                                            else:
                                                tempList.append("")
                                        else:
                                            tempList.append("")
                                        approved = sub_sub_section_con_data.approved
                                        approved_by = sub_sub_section_con_data.approved_by
                                        if approved_by is not None and  approved is True:
                                            tempList.append("approved")
                                        elif approved_by is not None and  approved is False:
                                            tempList.append("rejected")
                                        elif approved_by is  None and  approved is False:
                                            tempList.append("pending")
                                        else:
                                            tempList.append("")


                                        tag_id=OtherContributors.objects.get(id=sub_sub_section_con_data.content_contributors_id).tags.id
                                        if tag_id == "7":
                                            tempList.append("lod")
                                        elif tag_id == "11":
                                            tempList.append("lp")
                                        elif tag_id == "10":
                                            tempList.append("expr")
                                        elif tag_id == "9":
                                            tempList.append("expl")
                                        elif tag_id == "8":
                                            tempList.append("cq")
                                        else:
                                            tempList.append("")
                                        data_str_list.append( tempList)
                                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]


                                else:
                                    tempList.append(sub_sub_section_data.sub_sub_section)
                                    for i in range(7):
                                        tempList.append("")
                                    data_str_list.append(tempList)
                                

                                    tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
        for i in data_str_list:
            print(len(i))
        return data_str_list