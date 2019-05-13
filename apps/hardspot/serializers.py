from rest_framework import serializers
from .models import HardSpot,HardSpotContributors
from django.contrib.auth.models import User
# from user.models import EvolveUser
from apps.dataupload.models import Chapter,Section,SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword
from apps.configuration.models import Book
from apps.content.models import Content, ContentContributors




class ChapterSerializer(serializers.ModelSerializer):
    """Docstring for agegroupserializer."""

    class Meta:
        model = Chapter
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = "__all__"

#<-------------------------------------------------------------------------->
class SubSubSectionSerializer(serializers.ModelSerializer):
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
            count = HardSpot.objects.filter(sub_sub_section=req.id).count()
            return count
        except:
            return None

    def get_approved(self, req):
        try:
            sub_sec_approved = HardSpot.objects.filter(approved=True,sub_sub_section=req.id).count()
            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            sub_sec_reject = HardSpot.objects.filter(approved=False,sub_sub_section=req.id).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sub_sec_pending = HardSpot.objects.filter(approved=False,sub_sub_section=req.id,approved_by=None).count()
            return sub_sec_pending
        except:
            return None



class SubSectionSerializer(serializers.ModelSerializer):
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
            serializer = SubSubSectionSerializer(sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None

    def get_total(self, req):
        try:
            count = HardSpot.objects.filter(sub_section=req.id).count()
            return count
        except:
            return None

    def get_approved(self, req):
        try:
            sub_sec_approved = HardSpot.objects.filter(approved=True,sub_section=req.id).count()
            return sub_sec_approved
        except:
            return None

    def get_reject(self, req):
        try:
            sub_sec_reject = HardSpot.objects.filter(approved=False,sub_section=req.id).exclude(approved_by=None).count()
            return sub_sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sub_sec_pending = HardSpot.objects.filter(approved=False,sub_section=req.id,approved_by=None).count()
            return sub_sec_pending
        except:
            return None

class SectionNestedSerializer(serializers.ModelSerializer):
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
            serializer = SubSectionSerializer(sub_section_data, many=True)
            data = serializer.data
            return data
        except:
            return None
    def get_total(self, req):
        try:
            count = HardSpot.objects.filter(section=req.id).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            sec_approved = HardSpot.objects.filter(approved=True,section=req.id).count()
            return sec_approved
        except:
            return None
    def get_reject(self, req):
        try:
            sec_reject = HardSpot.objects.filter(approved=False,section=req.id).exclude(approved_by=None).count()
            return sec_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            sec_pending = HardSpot.objects.filter(approved=False,section=req.id,approved_by=None).count()
            return sec_pending
        except:
            return None

class ChapterNestedSerializer(serializers.ModelSerializer):
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
            serializer = SectionNestedSerializer(section_data, many=True)
            data = serializer.data
            return data
        except:
            return None

    def get_total(self, req):
        try:
            count = HardSpot.objects.filter(chapter=req.id).count()
            return count
        except:
            return None
    def get_approved(self, req):
        try:
            chapter_approved = HardSpot.objects.filter(approved=True,chapter=req.id).count()
            return chapter_approved
        except:
            return None
    def get_reject(self, req):
        try:
            chapter_reject = HardSpot.objects.filter(approved=False,chapter=req.id).exclude(approved_by=None).count()
            return chapter_reject 
        except:
            return None
    def get_pending(self, req):
        try:
            chapter_pending = HardSpot.objects.filter(approved=False,chapter=req.id,approved_by=None).count()
            return chapter_pending
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
#<----------------------------------------------------------------------------->

class HardSpotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardSpot
        fields='__all__'



class HardSpotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardSpot
        fields='__all__'

    def update(self, instance, validated_data):
        instance.approved = validated_data.get('approved', instance.approved)
        instance.approved_by=self.context.get('user', None)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance
   


class HardspotVisitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardSpotContributors
        fields = ['first_name',
                'last_name',
                'mobile',
                'email']

class ContentVisitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentContributors
        fields = ['first_name',
                'last_name',
                'mobile',
                'email']


class HardSpotContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardSpotContributors
        fields='__all__'


class HardSpotDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=HardSpot
        fields=('hard_spot','description','points_to_be_covered','useful_to','rating','comment')

class ApprovedHardSpotSerializer(serializers.ModelSerializer):
    chapter=serializers.SerializerMethodField()
   
    class Meta:
        model = Chapter
       
        fields = ['chapter']

    

    def get_chapter(self, req):
        # import ipdb; ipdb.set_trace()
        data_str_list = []
        chapters=Chapter.objects.filter(id=req.id).first()
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        chapter_hardspot = HardSpot.objects.filter(chapter__id=chapters.id,approved=True)
        section = ""
        sub_section = ""
        sub_sub_section= ""
        tempList.append(section)
        tempList.append(sub_section)
        tempList.append(sub_sub_section)
        keyword = ""
        chapter_keyword = ChapterKeyword.objects.filter(chapter__id=chapters.id)
        for keys in chapter_keyword:
            keyword =  keyword + keys.keyword + ", "
        tempList.append(keyword)
        
        if chapter_hardspot.exists():
            serializer = HardSpotDownloadSerializer(chapter_hardspot, many=True)
            no_of_hardspot=len(serializer.data)
            if no_of_hardspot == 5:
                for data in serializer.data:
                    for key, value in data.items():
                        tempList.append(value)
            elif no_of_hardspot < 5:
                for data in serializer.data[:no_of_hardspot]:
                    for key, value in data.items():
                        tempList.append(value)
                for i in range(0,(6*(5-no_of_hardspot))):
                    tempList.append("")
            else:
                for data in serializer.data[:5]:
                    for key, value in data.items():
                        tempList.append(value)
            data_str_list.append( tempList )

        else:
            for x in range(0,30):
                tempList.append("")
       
            data_str_list.append( tempList )
        
        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]
        sections=Section.objects.filter(chapter=req).order_by('id')
        if sections.exists():
            for section_data in sections:
                tempList.append(section_data.section)
                sec_hardspot = HardSpot.objects.filter(section__id=section_data.id,approved=True)
                sub_section = ""
                sub_sub_section=""
                tempList.append(sub_section)
                tempList.append(sub_sub_section)

                keyword = ""
                section_keyword = SectionKeyword.objects.filter(section__id=section_data.id)
                for keys in section_keyword:
                    keyword = keyword + keys.keyword + ", "
                tempList.append(keyword)
                if sec_hardspot.exists():
              
                    
                    serializer = HardSpotDownloadSerializer(sec_hardspot, many=True)
                    no_of_hardspot=len(serializer.data)
                    if no_of_hardspot == 5:
                        for data in serializer.data:
                            for key, value in data.items():
                                tempList.append(value)
                    elif no_of_hardspot < 5:
                        for data in serializer.data[:no_of_hardspot]:
                            for key, value in data.items():
                                tempList.append(value)
                        for i in range(0,(6*(5-no_of_hardspot))):
                            tempList.append("")
                    else:
                        for data in serializer.data[:5]:
                            for key, value in data.items():
                                tempList.append(value)
                    data_str_list.append( tempList )
                    
                else:
                    for x in range(0,30):
                        tempList.append("")
                    data_str_list.append( tempList )
                
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter , section_data.section]  
            # tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter ]  

                sub_section=SubSection.objects.filter(section__id=section_data.id).order_by('id')   
                if sub_section.exists():
                    for sub_section_data in sub_section:
                        tempList.append( sub_section_data.sub_section )
                        sub_sub_section=""
                        tempList.append(sub_sub_section)
                        keyword = ""
                        sub_section_keyword = SubSectionKeyword.objects.filter(sub_section__id=sub_section_data.id)
                        for keys in sub_section_keyword:
                            keyword = keyword + keys.keyword + ", "
                        tempList.append(keyword)

                        sub_sec_hardspot = HardSpot.objects.filter(sub_section__id=sub_section_data.id,approved=True)
                        if sub_sec_hardspot.exists():
                           
                            serializer = HardSpotDownloadSerializer(sub_sec_hardspot, many=True)
                            no_of_hardspot=len(serializer.data)
                            if no_of_hardspot == 5:
                                for data in serializer.data:
                                    for key, value in data.items():
                                        tempList.append(value)
                            elif no_of_hardspot < 5:
                                for data in serializer.data[:no_of_hardspot]:
                                    for key, value in data.items():
                                        tempList.append(value)
                                for i in range(0,(6*(5-no_of_hardspot))):
                                    tempList.append("")
                            else:
                                for data in serializer.data[:5]:
                                    for key, value in data.items():
                                        tempList.append(value)
                            data_str_list.append( tempList )
                        else:
                            for x in range(0,30):
                                tempList.append("")
                            data_str_list.append( tempList )
                    # tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section, sub_section_data.sub_section]
                    
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section, sub_section_data.sub_section]

                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id) 
                        
                        if sub_sub_sections.exists():

                            for sub_sub_section in sub_sub_sections:
                                tempList.append( sub_sub_section.sub_sub_section )
                                keyword = ""

                                sub_sub_section_keyword = SubSubSectionKeyword.objects.filter(sub_sub_section__id=sub_sub_section.id)
                                
                                for keys in sub_sub_section_keyword:
                                    keyword = keyword + keys.keyword + ", "
                                tempList.append(keyword)

                                sub_sub_sec_hardspot = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section.id,approved=True).order_by('id')
                                if sub_sub_sec_hardspot.exists():
                                    serializer = HardSpotDownloadSerializer(sub_sub_sec_hardspot, many=True)
                                    no_of_hardspot=len(serializer.data)
                                    if no_of_hardspot == 5:
                                        for data in serializer.data:
                                            for key, value in data.items():
                                                tempList.append(value)
                                    elif no_of_hardspot < 5:
                                        for data in serializer.data[:no_of_hardspot]:
                                            for key, value in data.items():
                                                tempList.append(value)
                                        for i in range(0,(6*(5-no_of_hardspot))):
                                            tempList.append("")
                                    else:
                                        for data in serializer.data[:5]:
                                            for key, value in data.items():
                                                tempList.append(value)
                                    data_str_list.append( tempList )
                                else:
                                    for x in range(0,30):
                                        tempList.append("")
                                    data_str_list.append( tempList )
                                
                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
        for i in data_str_list:
            print(i)
            print(len(i))
                # import ipdb; ipdb.set_trace()
        return data_str_list




class HardspotStatusSerializer(serializers.ModelSerializer):
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
        total = HardSpot.objects.filter(chapter__id=chapters.id).count()
        approved = HardSpot.objects.filter(chapter__id=chapters.id, approved=True).count()
        rejected = HardSpot.objects.filter(chapter__id=chapters.id, approved=False).exclude(approved_by=None).count()
        pending = HardSpot.objects.filter(chapter__id=chapters.id, approved=False, approved_by=None).count()
        # hard_spot = HardSpot.objects.filter(chapter__id=chapters.id).count()
        tempList.append(total)
        tempList.append(approved)
        tempList.append(rejected)
        tempList.append(pending)
        # tempList.append(hard_spot)
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
                total = HardSpot.objects.filter(section__id=section_data.id).count()
                approved = HardSpot.objects.filter(section__id=section_data.id, approved=True).count()
                rejected = HardSpot.objects.filter(section__id=section_data.id, approved=False).exclude(approved_by=None).count()
                pending = HardSpot.objects.filter(section__id=section_data.id, approved=False, approved_by=None).count()
                # hard_spot = HardSpot.objects.filter(section__id=section_data.id).count()
                tempList.append(total)
                tempList.append(approved)
                tempList.append(rejected)
                tempList.append(pending)
                # tempList.append(hard_spot)
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
                        # tempList.append(hard_spot)
                        data_str_list.append( tempList )
                        # print("3:>>"+str(len(tempList)))                       
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        sub_sub_sections=SubSubSection.objects.filter(subsection__id=sub_section_data.id).order_by('id')
                        if sub_sub_sections.exists():
                            for sub_sub_section_data in sub_sub_sections:
                                tempList.append(sub_sub_section_data.sub_sub_section)
                                total = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id).count()
                                approved = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=True).count()
                                rejected = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=False).exclude(approved_by=None).count()
                                pending = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id, approved=False, approved_by=None).count()
                                # hard_spot = HardSpot.objects.filter(sub_sub_section__id=sub_sub_section_data.id).count()
                                tempList.append(total)
                                tempList.append(approved)
                                tempList.append(rejected)
                                tempList.append(pending)
                                # tempList.append(hard_spot)
                                data_str_list.append( tempList )

                                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section,sub_section_data.sub_section ]
                        tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter, section_data.section ]
                tempList = [ chapters.book.subject.grade.medium.state, chapters.book.subject.grade.medium, chapters.book.subject.grade, chapters.book.subject, chapters.book, chapters.chapter]
    
        return data_str_list

class HardspotContributorsSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    school_name=serializers.SerializerMethodField()
    city_name=serializers.SerializerMethodField()

    textbook_name = serializers.SerializerMethodField()
    class Meta:
        model = HardSpot
        fields = ['first_name',
                'last_name',
                'mobile',
                'email',
                'city_name',
                'school_name',
                'textbook_name']
    def get_first_name(self, obj):
        first_name=HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().first_name
        return first_name
    def get_last_name(self, obj):
        last_name=HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().last_name
        return last_name
    def get_mobile(self, obj):
        mobile=HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().mobile
        return mobile
    def get_email(self, obj):
        email=HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().email
        return email
    def get_school_name(self,obj):
        school_name = HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().school_name
        return school_name
    def get_city_name(self,obj):
        city_name = HardSpotContributors.objects.filter(id=obj.hardspot_contributor.id).first().city_name
        return city_name
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


class HardSpotSerializer(serializers.ModelSerializer):
    hardspot_contributor = serializers.SerializerMethodField()
    class Meta:
        model = HardSpot
        fields=['id','approved_by','hardspot_contributor','chapter','section','hard_spot','description','points_to_be_covered','useful_to','rating']

    def get_hardspot_contributor(self, req):
        contributor = HardSpotContributors.objects.filter(id=req.hardspot_contributor.id).first()
        if contributor is not None:
            serializer = HardSpotContributorSerializer(contributor)
            return serializer.data
        else:
            return None





















