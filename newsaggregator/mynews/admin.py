from django.contrib import admin

# Register your models here.
from mynews.models import Headline


#adding our model to the admin dashboard
admin.site.register(Headline)