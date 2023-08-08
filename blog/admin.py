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
    list_display_links = ('publish',) 
    list_editable = ["title","status"]
    # raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
