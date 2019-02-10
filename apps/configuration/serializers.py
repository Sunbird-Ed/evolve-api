from rest_framework import routers, serializers
from .models import State,Medium,Grade,Subject,Book
from apps.dataupload.models import Chapter,Section,SubSection
from apps.hardspot.models import HardSpot
from apps.content.models import Content
from .models import State,Medium,Grade,Subject,Book


class DetailListSerializer(serializers.ModelSerializer):
    total_hardspot=serializers.SerializerMethodField()
    approved_hardspot=serializers.SerializerMethodField()
    total_content=serializers.SerializerMethodField()
    approved_content=serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = '__all__'
        depth=3

    def get_total_hardspot(self,req):
        chapter_count=HardSpot.objects.filter(chapter__book__id=req.id).count()
        section_count=HardSpot.objects.filter(section__chapter__book__id=req.id).count()
        subsection_count=HardSpot.objects.filter(sub_section__section__chapter__book__id=req.id).count()
        return(chapter_count + section_count + subsection_count)

    def get_approved_hardspot(self,req):
        chapter_count=HardSpot.objects.filter(chapter__book__id=req.id,approved=True).count()
        section_count=HardSpot.objects.filter(section__chapter__book__id=req.id,approved=True).count()
        subsection_count=HardSpot.objects.filter(sub_section__section__chapter__book__id=req.id,approved=True).count()
        return(chapter_count + section_count + subsection_count)

    def get_total_content(self,req):
        chapter_count=Content.objects.filter(chapter__book__id=req.id).count()
        section_count=Content.objects.filter(section__chapter__book__id=req.id).count()
        subsection_count=Content.objects.filter(sub_section__section__chapter__book__id=req.id).count()
        return(chapter_count + section_count + subsection_count)
        

    def get_approved_content(self,req):
        chapter_count=Content.objects.filter(chapter__book__id=req.id,approved=True).count()
        section_count=Content.objects.filter(section__chapter__book__id=req.id,approved=True).count()
        subsection_count=Content.objects.filter(sub_section__section__chapter__book__id=req.id,approved=True).count()
        return(chapter_count + section_count + subsection_count)



class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class MediumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium
        fields = '__all__'


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'