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
    path('create_club/',views.create_club, name='create_club'),
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/applied/', views.clubs_applied_to_list, name='clubs_applied_to_list'),
    path('clubs/joined/', views.clubs_joined_list, name='clubs_joined_list'),
    path('club/<str:club_pk>/', views.show_club, name='show_club'),
    path('club/<str:club_pk>/apply/', views.apply_Club, name='apply_Club'),
    path('club/<str:club_pk>/leave/', views.leave_club, name='leave_club'),
    path('club/<str:club_pk>/applicants/', views.applicant_list, name='applicants'),
    path('club/<str:club_pk>/change_details/', views.change_club_details, name='change_club_details'),
    path('club/<str:club_pk>/delete/', views.delete_club, name='delete_club'),
    path('club/<str:club_pk>/user/<int:user_id>/', views.show_user, name='show_user'),
    path('club/<str:club_pk>/user/<int:user_id>/to_member/', views.to_member, name='to_member'),
    path('club/<str:club_pk>/user/<int:user_id>/to_officer/', views.to_officer, name='to_officer'),
    path('club/<str:club_pk>/user/<int:user_id>/transfer_ownership/', views.transfer_ownership, name='transfer_ownership'),
    path('club/<str:club_pk>/user/<int:user_id>/remove/', views.remove_user, name='remove_user'),
]
