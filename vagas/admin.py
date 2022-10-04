from django.contrib import admin

from .models import Vaga


@admin.register(Vaga)
class AppApiAccessAdmin(admin.ModelAdmin):
    list_display = (
        "ubs",
        "fonte",
        # "endereco",
        "carga_horaria",
        # "salario_base",
        "especialidades",
        "created",
        "modified",
    )
    list_filter = (
        "carga_horaria",
        "especialidades",
        "fonte",
    )
