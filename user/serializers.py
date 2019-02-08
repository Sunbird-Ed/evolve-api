from rest_framework import routers, serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import EvolveUser,UserDetails,Roles
from apps.configuration.models import State


class UserDetailSerializer(ModelSerializer):
    user=serializers.SerializerMethodField()
    role=serializers.SerializerMethodField()
    state=serializers.SerializerMethodField()
    class Meta:
        model = UserDetails
        fields = ['role','user','state']

    def get_user(self,req):
        # import ipdb; ipdb.set_trace()
        user = EvolveUser.objects.filter(id=req.user.id)
        serializer=UserSerializer(user,many=True)
        return serializer.data

    def get_state(self,req):
        role = State.objects.filter(id=req.state.id)
        serializer=StateSerializer(role,many=True)
        return serializer.data

    def get_role(self,req):
        user = Roles.objects.filter(id=req.role.id)
        serializer=RoleSerializer(user,many=True)
        return serializer.data



class UserSerializer(ModelSerializer):
    class Meta:
        model=EvolveUser
        fields=['id','username','is_active','groups']

class StateSerializer(ModelSerializer):
    class Meta:
        model=State
        fields='__all__'

class RoleSerializer(ModelSerializer):
    class Meta:
        model=Roles
        fields='__all__'




        



