from django.contrib import admin

from central.models import Avaliacao, Cuidador, Paciente, Turno

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Cuidador)
admin.site.register(Avaliacao)
admin.site.register(Turno)
