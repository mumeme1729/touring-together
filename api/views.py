from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from django.db.models import Q
from .models import Profile,Plan,Comment,Relationship

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    #新規でプロフィールを作る
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)

class MyProfileListView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer
    #ログインしているユーザーのプロフィールを返す
    def get_queryset(self):
        queryset=Profile.objects.filter(userProfile=self.request.user)
        return queryset

class AllProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

#選択したプロフィールを返す
class SelectProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filter_class =serializers.SelectProfileSerializer

#プランを取得
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by('-created_on')
    serializer_class = serializers.PlanSerializer
    
    def perform_create(self, serializer):
        serializer.save(userPlan=self.request.user)


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.order_by('-created_on')
    serializer_class = serializers.PlanSerializer
    #検索結果
    def get_queryset(self):
        queryset = Plan.objects.order_by('-created_on')
        return queryset

class SearchPlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    filter_class =serializers.SearchPlanSerializer
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)

class GetCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_class =serializers. GetCommentSerializer

#フォロー

class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class =serializers.RelationshipSerializer
    def perform_create(self,serializer):
        serializer.save(userFollow=self.request.user)

class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = serializers.RelationshipSerializer
    filter_class =serializers.FollowingSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = serializers.RelationshipSerializer
    filter_class =serializers.FollowerSerializer


##  フォローしている人の投稿を取得する  ###
class TimelineView(generics.ListAPIView):
    serializer_class = serializers.PlanSerializer
    #検索結果
    def get_queryset(self):
        queryset = Plan.objects.filter(Q(userPlan__following__userFollow=self.request.user) | Q(userPlan=self.request.user))
        return queryset.order_by('-created_on')
