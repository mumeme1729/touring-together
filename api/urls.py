from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name='user'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet)
router.register('plan', views.PlanViewSet)
router.register('comment', views.CommentViewSet)
router.register('relationship',views.RelationshipViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('planlistview/',views.PlanListView.as_view(),name='planlistview'),
    path('follower/',views.FollowerViewSet.as_view(),name='follower'),
    path('',include(router.urls))
]
