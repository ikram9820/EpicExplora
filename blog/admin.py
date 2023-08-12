from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','status','publish',"body",'author']
    list_filter = ["status","publish","author"]
    search_fields= ["title","body"]
    prepopulated_fields = {"slug":("title",)}
    list_editable = ["status"]
    # raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

