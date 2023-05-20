from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Proveedor
from .forms import FormProveedor,FiltrosProveedor
from django.core.paginator import Paginator

class ListaProveedores(LoginRequiredMixin,ListView):
    #permission_required='materias.permiso_alumno'
    model=Proveedor
    paginate_by=10
    extra_context = {'form': FiltrosProveedor}

class NuevoProveedor(CreateView):
    #permission_required='materias.permiso_alumno' #temporalmente
    model = Proveedor
    form_class = FormProveedor
    # fields = '_all_'
    success_url = reverse_lazy('lista_proveedores')
    extra_context = {'accion': 'Nueva'}

def editar_proveedor(request, clave):
    proveedor = Proveedor.objects.get(clave=clave)
    
    if request.method == 'POST':
        form = FormProveedor(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = FormProveedor(instance=proveedor)
            
    context = {
        'form' : form
    }   
    return render(request, 'editar_proveedor.html', context)

    
def eliminar_proveedor(request, clave):
    Proveedor.objects.get(clave=clave).delete()
    return redirect('lista_proveedores')


def buscar_proveedor(request):
    proveedores = Proveedor.objects.all().order_by('-nombreEmpresa','nombreSupervisor')
    
    if request.method == 'POST':
        
        form = FiltrosProveedor(request.POST)
        clave = request.POST.get('clave',None)
        nombreEmpresa = request.POST.get('nombreEmpresa',None)
        rfc=request.POST.get('rfc',None)
        nombreSupervisor=request.POST.get('nombreSupervisor',None)
        diasPedido=request.POST.get('diasPedido',None)
        diasSurtido=request.POST.get('diasSurtido',None)
        Descripcion=request.POST.get('Descripcion',None)
        
        if clave:
            proveedores = proveedores.filter(clave=clave)
        if nombreEmpresa:
            # materias = materias.filter(nombre__startswith=nombre)
            proveedores = proveedores.filter(nombreEmpresa__contains=nombreEmpresa)
            proveedores = proveedores.filter(nombreEmpresa__icontains=nombreEmpresa)
            # materias = materias.get(nombre=nombre)
            
        if rfc:
            proveedores = proveedores.filter(rfc=rfc)
        
        if nombreSupervisor:
            proveedores = proveedores.filter(nombreSupervisor__contains=nombreSupervisor)
            proveedores = proveedores.filter(nombreSupervisor__icontains=nombreSupervisor)
        
        if diasPedido:
            proveedores = proveedores.filter(diasPedido=diasPedido)

        if diasSurtido:
            proveedores = proveedores.filter(diasSurtido=diasSurtido)
        
        if Descripcion:
            proveedores = proveedores.filter(Descripcion__contains=Descripcion)
            proveedores = proveedores.filter(Descripcion__icontains=Descripcion)
        
            
        print(proveedores.query)
            
    else:
        form = FiltrosProveedor()
        
    paginator = Paginator(proveedores, 2)  # Show 25 contacts per page.
    page_number = request.POST.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'form': form
    } 
    
    return render(request, 'Proveedores/proveedor_list.html', context)

def eliminar_todas(request):
    variable_names = list(request.POST.keys())
    if(len(variable_names)!=0):
        variable_names.pop(0)
        #print(variable_names)
        #print(dict[request.POST])
        if(len(variable_names)!=0):
            for clave in variable_names:
                Proveedor.objects.get(clave=clave).delete()
    return redirect('lista_proveedores')





