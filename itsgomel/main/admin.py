from django.contrib import admin

from .models import Mural, Comment, MuralSuggestion, NewsImage, News, ImprovementGallery, College, CollegeImage, History, HistoryImage

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

class CollegeImageInline(admin.TabularInline):
    model = CollegeImage
    extra = 1

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    inlines = [CollegeImageInline]

@admin.register(CollegeImage)
class CollegeImageAdmin(admin.ModelAdmin):
    list_display = ("college_news", "image")

class HistoryImageInline(admin.TabularInline):
    model = HistoryImage
    extra = 1

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    inlines = [HistoryImageInline]

@admin.register(HistoryImage)
class HistoryImageAdmin(admin.ModelAdmin):
    list_display = ("history", "image")

@admin.register(ImprovementGallery)
class ImprovementGalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "description")
    list_filter = ("date",)