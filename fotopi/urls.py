"""
URL configuration for fotopi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fotopiapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignupView.as_view(),name="signup"),
    path('login/',views.SigninView.as_view(),name="signin"),
    path('logout/',views.SignOutView.as_view(),name="signout"),
    path('',views.HomeView.as_view(),name="home"),
    path('userprofile/',views.UserProfileView.as_view(),name="userprofile"),
    path('userprofile/edit/',views.UserProfileUpdateView.as_view(),name="profile-update"),
    path('post/add/',views.PostUploadView.as_view(),name="post-add"),
    path('post/comment/<int:pk>/',views.CommentCreateView.as_view(),name="comment-add"),
    path('post/comment/all/<int:pk>/',views.CommentListView.as_view(),name="comment-list"),
    path('post/like/<int:pk>/',views.PostLikeView.as_view(),name="like"),
    path('profile/all/',views.ProfileListView.as_view(),name="profile-list"),
    path('profiles/<int:pk>/follow/',views.FollowView.as_view(),name="follow"),
    path('followers/all/',views.FollowersListView.as_view(),name="followers-list"),
    path('following/all/',views.FollowingListView.as_view(),name="following-list"),
    
  ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)