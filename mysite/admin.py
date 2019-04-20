from django.contrib import admin
from .models import Catelory,Post,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'catelory', 'author']
# Register your models here.
admin.site.register(Catelory)
admin.site.register(Post,PostAdmin)
admin.site.register(Tag)