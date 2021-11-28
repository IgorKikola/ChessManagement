"""ChessClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from chessManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/',views.sign_up, name='sign_up'),
    path('log_in/',views.log_in, name='log_in'),
    path('profile/',views.profile, name='profile'),
    path('change_password/',views.change_password, name='change_password'),
    path('change_profile/',views.change_profile, name='change_profile'),
    path('log_out/', views.log_out, name='log_out'),
    path('clubs/', views.club_list, name='club_list'),
    path('club/<str:pk>/', views.show_club_and_user_list, name='show_club_and_user_list'),
    path('owner_manage_club/<str:pk>/', views.owner_manage_club, name='owner_manage_club'),
    path('officer_manage_club/<str:pk>/', views.officer_manage_club, name='officer_manage_club'),
    path('user/<int:user_id>/', views.show_user, name='show_user'),
    path('owner_manage_club_list/', views.owner_manage_club_list, name='owner_manage_club_list'),
    path('officer_manage_club_list/', views.officer_manage_club_list, name='officer_manage_club_list'),
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('applicant_show_user/<int:user_id>/', views.applicant_show_user, name='applicant_show_user'),
    path('manage_owner_show_user/<int:user_id>/', views.manage_owner_show_user, name='manage_owner_show_user'),
    path('to_member/<int:user_id>/', views.to_member, name='to_member'),
    path('to_officer/<int:user_id>/', views.to_officer, name='to_officer'),
    path('transfer_ownership/<int:user_id>/', views.transfer_ownership, name='transfer_ownership'),
    path('create_club/',views.create_club, name='create_club'),
    path('apply_club/<str:pk>/', views.apply_Club, name='apply_Club'),
]
