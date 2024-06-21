from django.contrib import admin
from .models import *


# Register your models here.

class MeetupAdmin(admin.ModelAdmin):
  list_display=('title','organizer_email', 'meetup_date')
  prepopulated_fields={'slug':('title',)}
  list_filter=('title','meetup_date',)

admin.site.register(myUser)
admin.site.register(Participant)
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Speaker)


