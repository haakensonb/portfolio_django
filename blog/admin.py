from django.db import models
from django.contrib import admin

from markdownx.widgets import AdminMarkdownxWidget

from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    model = Post
    filter_horizontal = ('tags',)
    # Don't show author because it will be added by the save_model method
    exclude = ['author']

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget}
    }

    def save_model(self, request, obj, form, change):
        """
        On save, take the empty author attribute and set
        it to the current user housed in the request object
        """
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
