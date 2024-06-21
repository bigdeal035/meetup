from django.urls import path
from . import views
from .views import * 
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.index, name='meetups'),
    path('user-meetup/', views.userMeetups, name='user-meetup'),
    path('profile/', views.profile, name='user-profile'),
    path('contact/', Contact.as_view(), name='contact' ),
    path('contact/success/',views.contact_success, name='contact_success' ),

    path('add-speaker/<slug:meetup_slug>', views.addSpeaker, name='add-speaker'),
    path('speaker-details/<int:id>', views.speakerDetails, name='speaker-details'),
    path('speaker-update/<int:pk>', SpeakerUpdate.as_view(), name='speaker-update'),
    path('speaker-delete/<int:pk>', SpeakerDelete.as_view(), name='speaker-delete'),
    path('user-speaker/', views.userSpeaker, name='user-speaker'),
    path('meetup-details/<slug:meetup_slug>', views.meetup_details, name='meetup-details'),
    path('meetup-create', MeetupsCreate.as_view() , name='meetup-create'),
    path('meetup-update/<slug:slug>', MeetupUpdate.as_view() , name='meetup-update'),
    path('meetup-delete/<slug:slug>', MeetupDelete.as_view() , name='meetup-delete'),
    path('participants/<int:id>', views.participant, name='participants'),
    path('confirm/',views.confirmParticipation, name='confirm-registration'),
   


]

#http://127.0.0.1:8000/meetup-details/for-all-devoloper
#http://127.0.0.1:8000/meetup-update/my-meetups