from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.db.models import Q
from.forms import DatosPersonalesForm, CapacidadesForm, PuestoForm
from .models import DatosPersonales, Capacidades, Puesto
from django.contrib.auth.decorators import login_required




# Create your views here.

#?----------------------------------------------------------------------


def home(request):
    return render(request, 'home.html')

#?---------------------- Sign up, log in, log out -----------------------------

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(guardias)
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error" : 'Este usuario ya existe'
                })
        return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error" : 'Contraseñas no coinciden'
                })
        

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'El usuario o la contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('home')
        

@login_required
def signout(request):
    logout(request)
    return redirect('home')

#? --------------------------------------------------------------------------


#! Barra de busqueda (que se pueda buscar por puesto)

#! Deploy

@login_required
def guardias(request):
    query = request.GET.get('q') #query es la variable asignada a la busqueda de datos

    datos_personales = DatosPersonales.objects.all()
    capacidades = Capacidades.objects.all()
    puestos = Puesto.objects.all()
    
   #! hacer que en la busqueda tambien se pueda buscar por puesto
    if query:
        # Utilizar Q objects para realizar una búsqueda en varios campos
        datos_personales = datos_personales.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(cedula__icontains=query) |
            Q(telefono__icontains=query)
        )
        capacidades = capacidades.filter(
            datos_personales__in=datos_personales
        )
        puestos = puestos.filter(
            datos_personales__in=datos_personales or 
            Q(puesto_asignado__icontains=query)
            
        )
    
    #combina la informacion de las tres tablas
    guardias_datos = zip(datos_personales, capacidades, puestos)
    return render(request, 'guardias.html',{
        'guardias_datos' : guardias_datos,
        'query': query
    })



@login_required
def crear_guardia(request):
    if request.method == 'GET':
        return render(request, 'crear_guardia.html',{
            'form_crear_datos_personales' : DatosPersonalesForm
        })
    else:
        try:
            form = DatosPersonalesForm(request.POST)
            guardia = form.save(commit=False)
            guardia.user = request.user
            guardia.save()
            
            return redirect('guardias_detalle', guardia_id=guardia.id)
        except ValueError:
            return render(request, 'crear_guardia.html',{
                'form_crear_datos_personales' : DatosPersonalesForm,
                'error': 'Por favor ingresa datos válidos'
            })
  


@login_required            
def guardia_detalle(request, guardia_id):
    if request.method == 'GET':
        DatosPersonalesGuardia = get_object_or_404(DatosPersonales, pk = guardia_id)
        FormDatosPersonales = DatosPersonalesForm(instance=DatosPersonalesGuardia)
          
        try: 
        
            capacidades = get_object_or_404(Capacidades, datos_personales=DatosPersonalesGuardia.pk)
            FormCapacidadess = CapacidadesForm(datos_personales_default=DatosPersonalesGuardia, instance=capacidades)

            puesto = get_object_or_404(Puesto, datos_personales=DatosPersonalesGuardia.pk)
            FormPuesto = PuestoForm(datos_personales_default=DatosPersonalesGuardia, instance=puesto)
            
            return render(request, 'guardia_detalle.html', {
                'DatosPersonalesGuardia' : DatosPersonalesGuardia,
                'FormDatosPersonales' : FormDatosPersonales,
                'FormCapacidades' : FormCapacidadess,
                'FormPuesto' : FormPuesto
            })
            
        except:
        
            FormCapacidadess = CapacidadesForm(datos_personales_default=DatosPersonalesGuardia)
            FormPuesto = PuestoForm(datos_personales_default=DatosPersonalesGuardia)
            return render(request, 'guardia_detalle.html', {
                'DatosPersonalesGuardia' : DatosPersonalesGuardia,
                'FormDatosPersonales' : FormDatosPersonales,
                'FormCapacidades' : FormCapacidadess,
                'FormPuesto' : FormPuesto
            })
    else:
        
        try: 
            #! Modificar para que se actualice y no se cree otra aparte
            
            try:
                DatosPersonalesGuardia = get_object_or_404(DatosPersonales, pk = guardia_id)
                FormDatosPersonales = DatosPersonalesForm(request.POST, instance=DatosPersonalesGuardia)
                
                capacidades = get_object_or_404(Capacidades, datos_personales=DatosPersonalesGuardia)
                FormCapacidadess = CapacidadesForm(request.POST, instance=capacidades)

                puesto = get_object_or_404(Puesto, datos_personales=DatosPersonalesGuardia)
                FormPuesto = PuestoForm(request.POST, instance=puesto)
                
                FormDatosPersonales.save()
                FormCapacidadess.save()
                FormPuesto.save()
                return redirect('guardias')
            
            except:
                
                DatosPersonalesGuardia = get_object_or_404(DatosPersonales, pk = guardia_id)
                FormDatosPersonales = DatosPersonalesForm(request.POST, instance=DatosPersonalesGuardia)
            
                FormCapacidadess = CapacidadesForm(request.POST, datos_personales_default=DatosPersonalesGuardia)
                FormPuesto = PuestoForm(request.POST, datos_personales_default=DatosPersonalesGuardia)
                
                FormDatosPersonales.save()
                FormCapacidadess.save()
                FormPuesto.save()
                return redirect('guardias')
            
        except ValueError:
             try:
                 capacidades = get_object_or_404(Capacidades, datos_personales=DatosPersonalesGuardia.pk)
                 FormCapacidadess = CapacidadesForm(datos_personales_default=DatosPersonalesGuardia, instance=capacidades)

                 puesto = get_object_or_404(Puesto, datos_personales=DatosPersonalesGuardia.pk)
                 FormPuesto = PuestoForm(datos_personales_default=DatosPersonalesGuardia, instance=puesto)
                
            
                 return render(request, 'guardia_detalle.html', {
                     'DatosPersonalesGuardia' : DatosPersonalesGuardia,
                     'FormDatosPersonales' : FormDatosPersonales,
                     'FormCapacidades' : FormCapacidadess,
                     'FormPuesto' : FormPuesto,
                     'error' : 'Error al actualizar los datos'
                     })
             except:
                 FormCapacidadess = CapacidadesForm(datos_personales_default=DatosPersonalesGuardia)
                 FormPuesto = PuestoForm(datos_personales_default=DatosPersonalesGuardia)
                 return render(request, 'guardia_detalle.html', {
                     'DatosPersonalesGuardia' : DatosPersonalesGuardia,
                     'FormDatosPersonales' : FormDatosPersonales,
                     'FormCapacidades' : FormCapacidadess,
                     'FormPuesto' : FormPuesto,
                     'error' : 'Error al actualizar los datos'
                     })
                


@login_required 
def eliminar_guardia(request, guardia_id):
    guardia= get_object_or_404(DatosPersonales, pk = guardia_id)
    if request.method == 'POST':
        guardia.delete()
        return redirect('guardias')

    