from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile,Plan,Comment,Relationship

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model=Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        extra_kwargs = {'userProfile': {'read_only': True}}

class PlanSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Plan
        fields = ('id', 'destination', 'date','userPlan' ,'created_on', 'text',)
        extra_kwargs = {'userPost': {'read_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','plan')
        extra_kwargs = {'userComment': {'read_only': True}}

class  RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model= Relationship
        fields=('id','follow','follower')