# Register your models here.
from django.contrib import admin

from comments.models import Comment

admin.site.register(Comment)
