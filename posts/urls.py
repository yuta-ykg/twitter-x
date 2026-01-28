from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]
