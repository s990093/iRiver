from django.contrib import admin
from myapp.models import Post
from .models import music
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('name','slug', 'pub_date')

admin.site.register(Post, PostAdmin)



admin.site.register(music)