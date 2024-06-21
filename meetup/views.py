from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import Meetup, myUser
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from.forms import *
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from string import punctuation
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
#login user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('meetups')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        email.lower()
        try:
            user=myUser.objects.get(email=email)
        except:
            messages.error(request, ' user name does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('meetups')
        else:
            messages.error(request, 'invalid credential')
    return render(request, 'meetup/login.html')




def register(request):
    form=MyUserRegistrationForm()
    if request.method=='POST':
        form=MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('meetups')
        else:
             messages.error(request, 'An error occurred during registration')

    return render(request, 'meetup/register.html', {'form':form})

def index(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.filter(
        Q(title__icontains=q)|
          Q(description__icontains=q)|
          Q(location_name__icontains=q)
       
        )
    
    count=meetups.count()
   # user=myUser.objects.get(id=request.user.id)
    return render(request, 'meetup/index.html' , {'meetups':meetups, 'count':count})

def meetup_details(request, meetup_slug):
 selected_meetup=Meetup.objects.get(slug=meetup_slug)
 speakers=selected_meetup.meetup_speakers.all
 if request.method=='GET':
     form=ParticipantForm()
 else:
      form=ParticipantForm(request.POST)
      if form.is_valid():
          participant=form.save()
          selected_meetup.participant.add(participant)
          return redirect('confirm-registration')
 return render (request, 'meetup/meetup_detail.html', {'meetup':selected_meetup, 'speakers':speakers, 'form':form})

@login_required(login_url='login')
def userMeetups(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    user_meetups=Meetup.objects.order_by('-create')
    user_meetups=Meetup.objects.filter(activate=True)
    user_meetups=user_meetups.filter(user=request.user)

    user_meetups=user_meetups.filter(
        Q(title__icontains=q)|
          Q(description__icontains=q)|
          Q(location_name__icontains=q)
       
        )
    
    count=user_meetups.count()
    return render(request, 'meetup/user_meetup.html', {'user_meetups':user_meetups, 'count':count})

@login_required(login_url='login')
def addSpeaker(request, meetup_slug):
    selected_meetup=Meetup.objects.get(slug=meetup_slug)
    if request.method=='GET':
           form=SpeakerRegistration()
    else:
    
        form=SpeakerRegistration(request.POST, request.FILES)
        if form.is_valid():
                form.instance.user=request.user
                speaker=form.save(commit=False)
                form.instance.meetup_name=selected_meetup.title
                speaker=form.save()
                selected_meetup.meetup_speakers.add(speaker)
                return redirect('meetups')
              
    return render(request,'meetup/add_speaker.html',{'meetup':selected_meetup, 'form':form })

@login_required(login_url='login')
def userSpeaker(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    user_speakers=Speaker.objects.order_by('-id')
    user_speakers=user_speakers.filter(user=request.user)
    user_speakers= user_speakers.filter(
        Q(name__icontains=q)|
          Q(meetup_name__icontains=q)  
        )
    
    count=user_speakers.count()
    return render(request, 'meetup/user_speaker.html', {'user_speakers':user_speakers,'count':count})

@login_required(login_url='login')
def speakerDetails(request, id):
    speaker=Speaker.objects.get(pk=id)
    return render(request, 'meetup/speaker_details.html', {'speaker':speaker})


class MeetupUpdate(LoginRequiredMixin,UpdateView):
   model=Meetup
   form_class=UserMeetupForm
   template_name='meetup/meetup_form.html'
   success_url=reverse_lazy('meetups')
   slug_field='slug'
   def form_valid(self, form):
        form.instance.user=self.request.user
        return super(MeetupUpdate, self).form_valid(form)


#speakers update
class SpeakerUpdate(LoginRequiredMixin,UpdateView):
    model=Speaker
    form_class = SpeakerRegistration
    pk_url_kwarg='pk'
    template_name='meetup/add_speaker.html'
    success_url=reverse_lazy('meetups')
    
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerUpdate, self).form_valid(form)
    
#Delete Speakers
class SpeakerDelete(LoginRequiredMixin,DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='meetup/delete_speaker.html'
    success_url=reverse_lazy('user-speaker')

#Delete Meetups
class MeetupDelete(LoginRequiredMixin,DeleteView):
    model=Meetup
    context_object_name='meetup'
    slug_field='slug'
    template_name='meetup/delete_meetup.html'
    success_url=reverse_lazy('user-meetup')  

#add meetups class
class MeetupsCreate(LoginRequiredMixin,CreateView):
    model=Meetup
    form_class = UserMeetupForm
   
    success_url=reverse_lazy('meetups')
    template_name='meetup/meetup_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        for i in punctuation:
            form.instance.title=form.instance.title.replace(i, '')
        form.instance.slug=form.instance.title.replace(' ', '-').lower()
        return super(MeetupsCreate, self).form_valid(form)
    
@login_required(login_url='login')
def profile(request):
    page="Profile"
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    context={'form':form, 'page':page}
    return render(request, 'meetup/profile_form.html', context)

def confirmParticipation(request):
    return render (request, 'meetup/confirm.html')


def participant(request, id):
    selected_meetup=Meetup.objects.get(id=id)
    participants=selected_meetup.participant.all
    participants=selected_meetup.participant.order_by('-id')
    count=selected_meetup.participant.count()
    return render(request, 'meetup/participants.html', {'participants':participants, 'counts':count, 'meetup':selected_meetup})


class Contact(FormView):
    template_name = 'meetup/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

def contact_success(request):
    return render(request, 'meetup/contact_success.html')