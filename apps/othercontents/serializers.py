from rest_framework import routers, serializers
from .models import OtherContributors,OtherContent
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword,SubSubSection
from apps.configuration.models import Book


class OtherContributorSerializer(serializers.ModelSerializer):
	class Meta:
		model=OtherContributors
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
            contributions_approved=Content.objects.filter(sub_sub_section_id=req.id,approved=True,tag__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(sub_sub_section_id=req.id,approved=False,approved_by=None,tag__id = self.context.get('tagname', None)).count()
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
            contributions_approved=Content.objects.filter(sub_section_id=req.id,approved=True,tag__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(sub_section_id=req.id,approved=False,approved_by=None,tag__id = self.context.get('tagname', None)).count()
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
            contributions_approved=Content.objects.filter(section_id=req.id,approved =True,tag__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(section_id=req.id,approved=False,approved_by=None,tag__id = self.context.get('tagname', None)).count()
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
            contributions_approved=Content.objects.filter(chapter_id=req.id,approved=True,tag__id = self.context.get('tagname', None)).exclude(approved_by=None).count()
            contributions_pending=Content.objects.filter(chapter_id=req.id,approved=False,approved_by=None,tag__id = self.context.get('tagname', None)).count()
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