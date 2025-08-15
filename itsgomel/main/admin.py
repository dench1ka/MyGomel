from django.contrib import admin

from .models import Mural, Comment, MuralSuggestion, NewsImage, News

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

@admin.register(MuralSuggestion)
class MuralSuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'created_at')
    readonly_fields = ('created_at',)

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    inlines = [NewsImageInline]

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ("news", "image")