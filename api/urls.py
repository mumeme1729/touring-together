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
router.register('following',views.FollowingViewSet)
router.register('follower',views.FollowerViewSet)
router.register('selectprofile',views.SelectProfileViewSet)
router.register('getcomment',views.GetCommentViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('planlistview/',views.PlanListView.as_view(),name='planlistview'),
    path('user_profile/',views. AllProfileListView.as_view(),name='user_profile'),
    path('',include(router.urls)),
    path('timeline/',views.TimelineView.as_view(),name='timeline'),
]
