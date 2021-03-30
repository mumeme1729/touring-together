from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name='user'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
router.register('plan', views.PlanViewSet)
router.register('comment', views.CommentViewSet)
router.register('relationship',views.RelationshipViewSet)
router.register('searchplan',views.SearchPlanViewSet)
router.register('selectprofile',views.SelectProfileViewSet)
router.register('getcomment',views.GetCommentViewSet)
router.register('relation',views.RelationViewSet)
router.register('notification',views.NotificationViewSet)
router.register('likes',views.LikesViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('',include(router.urls)),
    path('timeline/',views.TimelineView.as_view(),name='timeline'),
    path('myfollowing_profile/',views.MyFollowingProfileView.as_view(),name='myfollowingprofile'),
    path('following_profile/',views.FollowingProfileView.as_view(),name='followingprofile'),
    path('follower_profile/',views.FollowerProfileView.as_view(),name='followerprofile'),
    path('userplan/',views.GetUserPlanSet.as_view(),name='userplan'),
    path('commentplan/',views.PlanCommnetView.as_view(),name='commentplan'),
    path('usernotification/',views.NotificationProfile.as_view(),name='usernotification'),
    path('prefectures/',views.PrefectureViewSet.as_view(),name='prefectures'),
    path('countlikes/',views.LikesView.as_view(),name='countlikes'),
    path('likedplans/',views. LikedPlanView.as_view(),name='likedplans'),
]
