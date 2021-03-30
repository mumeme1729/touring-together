from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile,Plan,Comment,Relationship,Notification,Prefectures,Likes
from django_filters import rest_framework as filters

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
        fields = ('id', 'nickName','text','userProfile', 'created_on', 'img','base')
        extra_kwargs = {'userProfile': {'read_only': True}}
    
class SelectProfileSerializer(filters.FilterSet):
    userProfile=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Profile
        fields=('userProfile',)


class PlanSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Plan
        fields = ('id','title','destination','prefecture','departure','date','userPlan' ,'created_on', 'text','img',)
        extra_kwargs = {'userPlan': {'read_only': True}}

class SearchPlanSerializer(filters.FilterSet):
    destination=filters.CharFilter(lookup_expr='contains')
    date=filters.DateFilter(lookup_expr='gte')
    prefecture=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Plan
        fields=('destination','date','prefecture')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','plan')
        extra_kwargs = {'userComment': {'read_only': True}}

class GetCommentSerializer(filters.FilterSet):
    plan=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Comment
        fields=('plan',)

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model= Relationship
        fields=('id','userFollow','following')
        extra_kwargs={'userFollow': {'read_only': True}}

class RelationfilterSerializer(filters.FilterSet):
    userFollow=filters.CharFilter(lookup_expr='exact')
    following=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Relationship
        fields=('userFollow','following')

class FollowingSerializer(filters.FilterSet):
    userFollow=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Relationship
        fields=('userFollow',)

class FollowerSerializer(filters.FilterSet):
    following=filters.CharFilter(lookup_expr='exact')
    class Meta:
        model=Relationship
        fields=('following',)

class LikesSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model= Likes
        fields=('id','plan','userLikes','created_on')
        extra_kwargs={'userFollow': {'read_only': True}}

class PlanProfileSerializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    class Meta:
        model =Plan
        fields = ('id','title','destination','prefecture','departure','date','userPlan' ,'created_on', 'text','img','profile','likes')
    
    def get_profile(self,obj):
        try:
            profile_abstruct_contents = ProfileSerializer(Profile.objects.filter(userProfile=obj.userPlan).first()).data
            return profile_abstruct_contents
        except:
            profile_abstruct_contents=None
            return profile_abstruct_contents
    
    def get_likes(self,obj):
        try:
            likes_abstruct_contents = LikesSerializer(Likes.objects.filter(plan=obj.id),many=True).data
            return likes_abstruct_contents
        except:
            likes_abstruct_contents=None
            return likes_abstruct_contents


class CommentProfileSerializer(serializers.ModelSerializer):
     profile=serializers.SerializerMethodField()
     
     class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','plan','profile')
    
     def get_profile(self,obj):
         try:
             profile_abstruct_contents = ProfileSerializer(Profile.objects.filter(userProfile=obj.userComment).first()).data
             return profile_abstruct_contents
         except:
             profile_abstruct_contents=None
             return profile_abstruct_contents

class NotificationSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    
    class Meta:
        model=Notification
        fields = ('id', 'status','receive','send', 'targetplan', 'created_on')
        
class NotificationProfileSerializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField()

    class Meta:
        model=Notification
        fields = ('id', 'status','receive','send', 'targetplan', 'created_on','profile')

    def get_profile(self,obj):
         try:
             profile_abstruct_contents = ProfileSerializer(Profile.objects.filter(userProfile=obj.send).first()).data
             return profile_abstruct_contents
         except:
             profile_abstruct_contents=None
             return profile_abstruct_contents


# 県
class PrefecturesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prefectures
        fields='__all__'


    
