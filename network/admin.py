from django.contrib import admin

# Register your models here.

from .models import User, Post, Comment, Relationship

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Relationship)