from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Plot)
admin.site.register(Campsite)
admin.site.register(Facility)
admin.site.register(Booking)