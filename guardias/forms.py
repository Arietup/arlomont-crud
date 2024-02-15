from django import forms

from .models import DatosPersonales, Capacidades, Puesto

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = '__all__'
        widgets = {
            'sexo': forms.Select(choices=DatosPersonales.sexos),
            'tipo_sangre': forms.Select(choices=DatosPersonales.tipos_sangre),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class CapacidadesForm(forms.ModelForm):
    
    def __init__(self, *args, datos_personales_default=None, **kwargs):
        super(CapacidadesForm, self).__init__(*args, **kwargs)
        if datos_personales_default:
            self.fields['datos_personales'].initial = datos_personales_default
            
    class Meta:
        model = Capacidades
        fields = '__all__'
        widgets = {
            'nivel_estudio': forms.Select(choices=Capacidades.niveles_estudio),
            'tipo_licencia': forms.Select(choices=Capacidades.tipos_licencia),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
        }

class PuestoForm(forms.ModelForm):
    def __init__(self, *args, datos_personales_default=None, **kwargs):
        super(PuestoForm, self).__init__(*args, **kwargs)
        if datos_personales_default:
            self.fields['datos_personales'].initial = datos_personales_default

    class Meta:
        model = Puesto
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
        }