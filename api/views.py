from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from django.db.models import Q
from .models import Profile,Plan,Comment,Relationship,Notification

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




#### ログインユーザーのフォローしている人のプロフィール
class MyFollowingProfileView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset=Profile.objects.filter(Q(userProfile=self.request.user) | Q(userProfile__following__userFollow=self.request.user))
        return queryset

###フォローしているユーザーのプロフィール
class FollowingProfileView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset=Profile.objects.filter(userProfile__following__userFollow=self.request.query_params.get('id'))
        return queryset
### フォロワーのプロフィール ####
class FollowerProfileView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset=Profile.objects.filter(userProfile__userFollow__following=self.request.query_params.get('id'))
        return queryset

### フォロー解除時の対象  ###
class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = serializers.RelationshipSerializer
    filter_class =serializers.RelationfilterSerializer
    
# タイムライン   
class TimelineView(generics.ListAPIView):
    serializer_class = serializers.PlanProfileSerializer
    #検索結果
    def get_queryset(self):
        queryset = Plan.objects.filter(Q(userPlan__following__userFollow=self.request.user)| Q(userPlan=self.request.user)).distinct()
        return queryset.order_by('-created_on')   

#サーチ
class SearchPlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all().order_by('-created_on') 
    serializer_class = serializers.PlanProfileSerializer
    filter_class =serializers.SearchPlanSerializer

#コメントを取得
class GetCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentProfileSerializer
    filter_class =serializers.GetCommentSerializer
   
## ユーザー詳細画面で表示する　##

## 自分の投稿 ##
class GetUserPlanSet(generics.ListAPIView):
    serializer_class =serializers.PlanSerializer

    def get_queryset(self):
        queryset=Plan.objects.filter(userPlan=self.request.query_params.get('id'))
        return queryset.order_by('-created_on')

# コメントした投稿
class PlanCommnetView(generics.ListAPIView):
    serializer_class = serializers.PlanProfileSerializer
   
    def get_queryset(self):
        queryset = Plan.objects.filter(plan__userComment=self.request.query_params.get('id')).distinct()
        return queryset.order_by('-created_on') 
        #return queryset

class NotificationViewSet(viewsets.ModelViewSet):
    queryset=Notification.objects.all().order_by('-created_on')
    serializer_class =serializers.NotificationSerializer

    def perform_create(self,serializer):
        serializer.save()

class NotificationProfile(generics.ListAPIView):
    serializer_class =serializers.NotificationProfileSerializer

    def get_queryset(self):
        queryset=Notification.objects.filter(receive=self.request.user).exclude(send=self.request.user)
        return queryset.order_by('-created_on')
