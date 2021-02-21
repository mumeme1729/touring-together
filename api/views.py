from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers

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
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    #ログインしているユーザーのプロフィールを返す
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    
    def perform_create(self, serializer):
        serializer.save(userPlan=self.request.user)


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    #検索結果
    def get_queryset(self):
        queryset = Plan.objects.all()
        destination = self.request.query_params.get('destination',None)
        
        if destination is not None:
            queryset =queryset.filter(destination__icontains=destination)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)

#フォロー
class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class =serializers.RelationshipSerializer

    def perform_create(self,serializer):
        serializer.save(userFollow=self.request.user)

#フォロワーのリスト
class FollowerViewSet(generics.ListAPIView):
    queryset = Relationship.objects.all()
    serializer_class = serializers.RelationshipSerializer
    #検索結果
    def get_queryset(self):
        return self.queryset.filter(following=self.request.user)
