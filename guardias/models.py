from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DatosPersonales(models.Model):
    cedula = models.CharField(max_length=10)
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    direccion_domiciliaria = models.TextField()
    sexos = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    sexo = models.CharField(max_length=1, choices=sexos, null=True, blank=True, default='M')
    correo_electronico = models.CharField(max_length=50, null=True, blank=True)
    
    tipos_sangre = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    tipo_sangre = models.CharField(max_length=3, choices=tipos_sangre)
    
    certificado_votacion = models.BooleanField()
    cargas_familiares = models.IntegerField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    discapacidad = models.BooleanField()
    
   
    
    def __str__(self) -> str:
        return self.cedula + self.apellidos 
    
class Capacidades(models.Model):
    datos_personales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    
    niveles_estudio = [
        ('Primario', 'Primario'),
        ('Secundario', 'Secundario'),
        ('Bachiller EN CURSO', 'Bachiller EN CURSO'),
        ('Bachiller', 'Bachiller'),
        ('Universitario EN CURSO', 'Universitario EN CURSO'),
        ('Universitario', 'Universitario'),
        ('Magister', 'Magister'),
    ]
    nivel_estudio = models.CharField(max_length=50, choices=niveles_estudio) 
    
    num_escuela_capacitacion = models.CharField(max_length=20)
    
    licencia_conducir = models.BooleanField()
    tipos_licencia = [
        ('No Aplica', 'No Aplica'),
        ('Tipo B', 'Tipo B (solo autos)'),
        ('Tipo Moto', 'Tipo Moto'),
        ('Tipo Profesional', 'Tipo Profesional'),
    ]
    tipo_licencia = models.CharField(max_length=30, choices=tipos_licencia, null=True, blank=True, default='No Aplica')
    
    record = models.BooleanField()
    certificado_salud = models.BooleanField()
    afis = models.BooleanField()
    cursos_seguridad = models.TextField(max_length=50, null=True, blank=True)
    libreta_militar = models.BooleanField()

class Puesto(models.Model):
    datos_personales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(null=True, blank=True)
    puesto_asignado = models.CharField(max_length=40, null=True, blank=True)
    Descripcion_puesto = models.TextField(max_length=100, null=True, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)
    razon_salida = models.TextField(max_length=100, null=True, blank=True)