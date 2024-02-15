from django.contrib import admin
from .models import DatosPersonales, Capacidades, Puesto

# Register your models here.
admin.site.register(DatosPersonales)
admin.site.register(Capacidades)
admin.site.register(Puesto)