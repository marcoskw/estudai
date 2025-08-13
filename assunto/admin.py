from django.contrib import admin
from .models import Assunto

@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'materia')
    list_filter = ('materia',)
    search_fields = ('nome',)