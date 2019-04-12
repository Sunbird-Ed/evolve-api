from rest_framework import routers, serializers
from .models import OtherContributors


class OtherContributorSerializer(serializers.ModelSerializer):
	class Meta:
		model=OtherContributors
		fields='__all__'