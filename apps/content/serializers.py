from rest_framework import routers, serializers
from .models import Content,ContentContributors
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword
from apps.configuration.models import Book
from apps.hardspot.models import HardSpot
from apps.hardspot.serializers import HardSpotCreateSerializer
from django.db.models import Q



class ContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

    def update(self, instance, validated_data):
        # import ipdb; ipdb.set_trace()
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by=self.context.get('user', None)
        instance.rating = self.validated_data.get('rating', instance.rating)
        instance.rated_by = self.context.get('user', None)
        instance.comment = self.validated_data.get('comment', None)
        instance.save()
        return instance


class ContentStatusListSerializer(serializers.ModelSerializer):
    hard_spot = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields="__all__"

    def get_hard_spot(self, req):
        try:
            # import ipdb;ipdb.set_trace()
            hardspot_data = HardSpot.objects.filter(id=req.hard_spot.id).first()
            serializer = HardSpotCreateSerializer(hardspot_data)
            data = serializer.data
            return data
        except:
            return None
    

class SubSectionSerializer(serializers.ModelSerializer):
    contributions_count=serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()

    class Meta:
        model = SubSection
        fields = ['id',
        'section',        
        'sub_section',
        'contributions_count',
        'hardspot_count'

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
            # contributions_count=Content.objects.filter(sub_section_id=req.id).count()
            # return contributions_count
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
                'hardspot_count']

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

            # contributions_count=Content.objects.filter(section_id=req.id).count()
            # return contributions_count
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
# class BookNestedSerializer(serializers.ModelSerializer):
class ChapterNestedSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    hardspot_count=serializers.SerializerMethodField()
    contributions_count=serializers.SerializerMethodField()


    class Meta:
        model = Chapter
        fields =['id','chapter','section','hardspot_count','contributions_count']

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
            # contributions_count=Content.objects.filter(chapter_id=req.id).count()
            # return contributions_count
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
            # import ipdb;ipdb.set_trace()
            chapter_data = Chapter.objects.filter(book=req.id)#.exclude(Q(book__hardspot_only=True) & ~Q(hardspot__isnull=False))
            serializer = ChapterNestedSerializer(chapter_data, many=True)
            data = serializer.data
            return data
        except:
            return None
#<------------------------------------------------------------------>

class ContentSubSectionSerializer(serializers.ModelSerializer):
    total=serializers.SerializerMethodField()
    approved=serializers.SerializerMethodField()
    reject=serializers.SerializerMethodField()
    pending=serializers.SerializerMethodField()

    class Meta:
        model = SubSection
        fields = ['id',
        'section',
        'total',
        'approved',
        'reject',
        'pending',
        'sub_section',
        ]

    
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
        # import ipdb;ipdb.set_trace()
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
            # import ipdb;ipdb.set_trace()
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
            # import ipdb;ipdb.set_trace()
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
            # import ipdb;ipdb.set_trace()
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
    # chapter_keywords=ChapterKeywordsSerializer(many=True)
    # section_keywords=SectionKeywordsSerializer(many=True)
    # sub_section_keywords=SubSectionKeywordsSerializer(many=True)
    keywords = serializers.SerializerMethodField()
    hard_spot = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = ('id','first_name','last_name', 'email','mobile','hard_spot','chapter','section','sub_section','content_name','video','approved','approved_by' ,'rating','rated_by','comment','keywords',)
    
    def get_hard_spot(self, req):
        try:
            # import ipdb;ipdb.set_trace()
            hardspot_data = HardSpot.objects.filter(id=req.hard_spot.id).first()
            serializer = HardSpotCreateSerializer(hardspot_data)
            data = serializer.data
            return data
        except:
            return None

    def get_keywords(self, obj):
        try:
            # import ipdb;ipdb.set_trace()
            # chapter_keywords = ChapterKeyword.objects.filter(chapter=obj.chapter)
            # section_keywords = SectionKeyword.objects.filter(section=obj.section)
            # sub_section_keywords = SubSectionKeyword.objects.filter(sub_section=obj.sub_section)
            if obj.chapter_keywords.all().exists():
                k=obj.chapter_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = ChapterKeywordsSerializer(ChapterKeyword.objects.filter(keyword__in=listValues), many=True)
                return serializer.data
            elif obj.section_keywords.all().exists():
                k=obj.section_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = SectionKeywordsSerializer(SectionKeyword.objects.filter(keyword__in=listValues), many=True)
                return serializer.data
            elif obj.sub_section_keywords.all().exists():
                k=obj.sub_section_keywords.all().values('keyword')
                listData = [ x for x in k ]
                listValues=[]
                for keyvalues in listData:
                    listValues.append( keyvalues['keyword'] )
                serializer = SubSectionKeywordsSerializer(SubSectionKeyword.objects.filter(keyword__in=listValues), many=True)
                return serializer.data
            else:
                return None
        except Exception as error:
            pass


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