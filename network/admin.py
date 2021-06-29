from django.contrib import admin

from .models import User, Post
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=[
        "username",

    ]

class PostAdmin(admin.ModelAdmin):
    list_display=[
        "author",

    ]

admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)