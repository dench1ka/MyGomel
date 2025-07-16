from django.contrib import admin
from .models import Mural

# Register your models here.
@admin.register(Mural)
class MuralAdmin(admin.ModelAdmin):
    list_display = ('title', 'address')