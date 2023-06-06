from django.contrib import admin
from .models import User,Snippet,Tag
# Register your models here.

admin.site.register(User)
admin.site.register(Snippet)
admin.site.register(Tag)
