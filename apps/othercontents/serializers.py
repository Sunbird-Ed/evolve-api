from rest_framework import routers, serializers
from .models import OtherContributors,OtherContent


class OtherContributorSerializer(serializers.ModelSerializer):
	class Meta:
		model=OtherContributors
		fields='__all__'



class OtherContentListSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=OtherContent
		fields='__all__'