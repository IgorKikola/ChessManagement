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
    path('club_home', views.club_list_home, name="club_list_home"),
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('log_out/', views.log_out, name='log_out'),
    path('clubs/', views.club_list, name='club_list'),
    path('user/<int:user_id>/', views.show_user, name='show_user'),
    path('users/', views.user_list, name='user_list'),
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('club/<club_name>/', views.club_profile, name='club_profile'),
    path('user/<int:user_id>/to_member/', views.to_member, name='to_member'),
    path('user/<int:user_id>/to_officer/', views.to_officer, name='to_officer'),
    path('user/<int:user_id>/transfer_ownership/', views.transfer_ownership, name='transfer_ownership'),
    path('clubs/<club_name>/<int:user_id>/apply', views.club_Application, name='club_Application'),
]
