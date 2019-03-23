from rest_framework import serializers
from .models import Chapter, Section, SubSection,SubSubSection
from apps.hardspot.models import HardSpot
from apps.content.models import Content
from apps.configuration.models import State, Book, Grade, Subject, Medium

class ChapterSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = Chapter
		fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Section
		fields = "__all__"

class SubSubSectionSerializer(serializers.ModelSerializer):
	hardspot_count = serializers.SerializerMethodField()
	content_count = serializers.SerializerMethodField()
	class Meta:
		model = SubSubSection
		fields = ['id',
		'subsection',
		'sub_sub_section',
		'hardspot_count',
		'content_count',
		'active']

	

	def get_hardspot_count(self, req):
		try:
			count = HardSpot.objects.filter(sub_sub_section=req.sub_sub_section.id).count()
			return count
		except:
			return None

	def get_content_count(self, req):
		try:
			count = Content.objects.filter(sub_sub_section=req.sub_sub_section.id).count()
			return count
		except:
			return None

class SubSectionSerializer(serializers.ModelSerializer):
	hardspot_count = serializers.SerializerMethodField()
	content_count = serializers.SerializerMethodField()
	sub_sub_section = serializers.SerializerMethodField()
	class Meta:
		model = SubSection
		fields = ['id',
		'sub_section',
		'section',
		'hardspot_count',
		'content_count',
		'active',
		'sub_sub_section']

	def get_sub_sub_section(self, req):
		try:
			sub_sub_section_data = SubSubSection.objects.filter(subsection=req.id).order_by('id')
			serializer = SubSubSectionSerializer(sub_sub_section_data, many=True)
			data = serializer.data
			return data
		except:
			return None

	def get_hardspot_count(self, req):
		try:
			count = HardSpot.objects.filter(sub_section=req.sub_section.id).count()
			return count
		except:
			return None

	def get_content_count(self, req):
		try:
			count = Content.objects.filter(sub_section=req.sub_section.id).count()
			return count
		except:
			return None

class SectionNestedSerializer(serializers.ModelSerializer):
	sub_section = serializers.SerializerMethodField()
	hardspot_count = serializers.SerializerMethodField()
	content_count = serializers.SerializerMethodField()
	class Meta:
		model = Section
		fields = ['id',
				'section',
				'hardspot_count',
				'content_count',
				'sub_section',
				'active']
	def get_sub_section(self, req):
		try:
			
			sub_section_data = SubSection.objects.filter(section=req.id).order_by('id')
			serializer = SubSectionSerializer(sub_section_data, many=True)
			data = serializer.data
			return data
		except:
			return None

	def get_hardspot_count(self, req):
		try:
			count = HardSpot.objects.filter(section=req.section.id).count()
			return count
		except:
			return None

	def get_content_count(self, req):
		try:
			count = Content.objects.filter(section=req.section.id).count()
			return count
		except:
			return None


class SubsectionNestedSerializer(serializers.ModelSerializer):
	sub_section = SectionNestedSerializer()
	class Meta:
		model = SubSection
		fields = ['id',
				'sub_section'
				'section']


class ChapterNestedSerializer(serializers.ModelSerializer):
	section = serializers.SerializerMethodField()
	hardspot_count = serializers.SerializerMethodField() 
	content_count = serializers.SerializerMethodField()
	
	

	class Meta:
		model = Chapter
		fields = ['id',
				'chapter',
				'hardspot_count',
				'content_count',
		        'section',
		        'active'
				]

	def get_section(self, req):
		try:
			
			section_data = Section.objects.filter(chapter=req.id).order_by('id')
			serializer = SectionNestedSerializer(section_data, many=True)
			data = serializer.data
			return data
		except:
			return None

	def get_hardspot_count(self, req):
		try:
			count = HardSpot.objects.filter(chapter=req.chapter.id).count()
			return count
		except:
			return None

	def get_content_count(self, req):
		try:
			count = Content.objects.filter(chapter=req.chapter.id).count()
			return count
		except:
			return None

class BookNestedSerializer(serializers.ModelSerializer):
	chapter = serializers.SerializerMethodField()
	
	

	class Meta:
		model = Book
		fields = ['id',
				'book',
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

class StateUploadSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = ['state']

class GradeUploadSerializer(serializers.ModelSerializer):
	state=StateUploadSerializer()
	class Meta:
		model = Grade
		fields = ['grade',
				'state']

class MediumUploadSerializer(serializers.ModelSerializer):
	grade=GradeUploadSerializer()
	class Meta:
		model = Medium
		fields = ['medium',
				'grade']

class SubjectUploadSerializer(serializers.ModelSerializer):
	medium=MediumUploadSerializer()
	class Meta:
		model = Subject
		fields = ['Subject',
				'medium']

class BookUploadSerializer(serializers.ModelSerializer):
	subject=SubjectUploadSerializer()
	class Meta:
		model = Book
		fields = ['book',
				'subject']

class ChapterUploadSerializer(serializers.ModelSerializer):
	book = BookUploadSerializer()
	class Meta:
		model = Chapter
		fields = ['chapter',
				'book']

class SectionUploadSerializer(serializers.ModelSerializer):
	chapter=ChapterUploadSerializer()
	class Meta:
		model = Section
		fields = ['section', 'chapter']



