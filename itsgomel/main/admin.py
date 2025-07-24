from django.contrib import admin

from .models import Mural, Comment

# Register your models here.
@admin.register(Mural)
class MuralAdmin(admin.ModelAdmin):
    list_display = ('title', 'address')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'created_at')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
    search_fields = ('name', 'text')