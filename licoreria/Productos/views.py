from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Producto,Tipo
from .forms import FormProducto,FiltrosProducto,FormExistencia,FiltrosVenta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Venta
from .forms import VentaForm



class ListaProductos(ListView):
    #permission_required='materias.permiso_alumno'
    model=Producto
    paginate_by=10
    extra_context = {'form': FiltrosProducto}

class NuevoProducto(CreateView):
    #permission_required='materias.permiso_alumno' #temporalmente
    model = Producto
    form_class = FormProducto
    # fields = '_all_'
    success_url = reverse_lazy('Producto:lista_productos')
    extra_context = {'accion': 'Nueva'}

def editar_producto(request, clave):
    producto = Producto.objects.get(clave=clave)
    
    if request.method == 'POST':
        form = FormProducto(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('Producto:lista_productos')
    else:
        form = FormProducto(instance=producto)
            
    context = {
        'form' : form
    }   
    return render(request, 'editar_producto.html', context)


def editar_productoExistencia(request, clave):
    producto = Producto.objects.get(clave=clave)

    if request.method == 'POST':
        # Remove the 'precio', 'categoria', 'tipo', and 'tamanio' fields from the form
        form = FormExistencia(request.POST)
        if form.is_valid():
            # Get the existing 'existencia' value
            existing_existencia = producto.existencia
            
            # Get the new 'existencia' value from the form
            new_existencia = form.cleaned_data['existencia']
            
            # Calculate the updated 'existencia' value
            updated_existencia = existing_existencia + new_existencia
            
            # Update the 'existencia' field of the 'producto' instance
            producto.existencia = updated_existencia
            producto.save()
            return redirect('Producto:lista_productos')
    else:
        # Create a new form with just the 'existencia' field
        form = FormExistencia(initial={'existencia': producto.existencia})
    
    context = {
        'form' : form,
        'producto': producto # Optionally pass the 'producto' instance to the context for display purposes
    }   
    return render(request, 'editar_productoExistencia.html', context)



    
def eliminar_producto(request, clave):
    Producto.objects.get(clave=clave).delete()
    return redirect('Producto:lista_productos')

class Bienvenido(TemplateView):
    template_name = 'home.html'


def buscar_materia(request):
    productos = Producto.objects.all().order_by('-nombre','precio')
    
    if request.method == 'POST':
        
        form = FiltrosProducto(request.POST)
        clave = request.POST.get('clave',None)
        nombre = request.POST.get('nombre',None)
        tamanio = request.POST.get('tamanio',None)
        precio = request.POST.get('precio',None)
        categoria = request.POST.get('categoria',None)
        tipo = request.POST.get('tipo',None)

        if clave:
            productos = productos.filter(clave=clave)
        if nombre:
            # materias = materias.filter(nombre__startswith=nombre)
            productos = productos.filter(nombre__contains=nombre)
            productos = productos.filter(nombre__icontains=nombre)
            # materias = materias.get(nombre=nombre)
            
        if tamanio:
            productos = productos.filter(tamanio=tamanio)
        if precio:
            productos = productos.filter(precio=precio)
        if categoria:
            productos = productos.filter(categoria=categoria)
        if tipo:
            tipo = productos.filter(tipo=tipo)
            
        print(productos.query)
            
    else:
        form = FiltrosProducto()
        
    paginator = Paginator(productos, 2)  # Show 25 contacts per page.
    page_number = request.POST.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'form': form
    } 
    
    return render(request, 'Productos/producto_list.html', context)

def eliminar_todas(request):
    variable_names = list(request.POST.keys())
    if(len(variable_names)!=0):
        variable_names.pop(0)
        #print(variable_names)
        #print(dict[request.POST])
        if(len(variable_names)!=0):
            for clave in variable_names:
                Producto.objects.get(clave=clave).delete()
    return redirect('Producto:lista_productos')



def busca_tipos(request):
    id_categoria=request.POST.get('id_categoria',None)
    if id_categoria:
        tipos=Tipo.objects.filter(categoria_id=id_categoria)
        data = [{'id':tipo.id,'nombre':tipo.nombre} for tipo in tipos]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error':'Parametro invalido'},safe=False)



######################################################## Ventas

from .models import Producto
#LoginRequieredMixin
class ListaVentas(ListView):
    model = Venta
    paginate_by = 10
    template_name = 'sales/list_ventas.html'
    context_object_name = 'ventas'
    extra_context = {'form': FiltrosVenta}


@login_required
def create_venta(request):
    user = request.user  # Assuming the user is authenticated # Get the current date

    # Create a new Venta object with the current date
    venta = Venta(usuario=user)
    venta.save()

    venta_pk = venta.pk
    return redirect('Producto:detalle_venta_list')

from .models import DetalleVenta
from .forms import DetalleVentaForm

def detalle_venta_list(request):
    detalle_venta = DetalleVenta.objects.all()
    return render(request, 'detalle_venta/list.html', {'detalle_venta': detalle_venta})

from django.shortcuts import render, get_object_or_404, redirect
from .models import DetalleVenta, Venta
from .forms import DetalleVentaForm

def detalle_venta_create(request):
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            detalle_venta = form.save(commit=False)  # Create the instance without saving to the database
            last_venta = Venta.objects.last()  # Retrieve the last Venta instance
            detalle_venta.id_venta = last_venta  # Assign the last Venta as id_venta
            detalle_venta.save()  # Save the instance with the assigned id_venta
            return redirect('Producto:detalle_venta_list')
    else:
        form = DetalleVentaForm()
    return render(request, 'detalle_venta/create.html', {'form': form})


def detalle_venta_update(request, pk):
    detalle_venta = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST, instance=detalle_venta)
        if form.is_valid():
            form.save()
            return redirect('detalle_venta_list')
    else:
        form = DetalleVentaForm(instance=detalle_venta)
    return render(request, 'detalle_venta/update.html', {'form': form})

def detalle_venta_delete(request, pk):
    detalle_venta = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'POST':
        detalle_venta.delete()
        return redirect('detalle_venta_list')
    return render(request, 'detalle_venta/delete.html', {'detalle_venta': detalle_venta})


def detalle_venta_view(request, id_venta):
    detalle_ventas = DetalleVenta.objects.filter(id_venta=id_venta)

    return render(request, 'detalle_venta.html', {'detalle_ventas': detalle_ventas})


    #return redirect('bienvenida', pk=venta_pk)


#def create_venta(request):
#    if request.method == 'POST':
#        form = VentaForm(request.POST)
#        if form.is_valid():
#            venta = form.save(commit=False)  # Get the unsaved form instance
#            producto = venta.producto
#            existencia = producto.existencia - venta.cantidad  # Assuming the field name is "quantity"
#            producto.existencia = existencia
#            producto.save()
#            form.save()
#            return redirect('Producto:list')
#    else:
#        form = VentaForm()
#    
#    return render(request, 'sales/create_venta.html', {'form': form})
#
#from .models import Venta
#
#def eliminar_venta(request, id):
#    venta = Venta.objects.get(id=id)
#
#    # Store the quantity for later use
#    cantidad = venta.cantidad
#
#    # Delete the venta
#    venta.delete()
#
#    # Reverse the subtraction
#    producto = venta.producto
#    producto.existencia += cantidad
#    producto.save()
#
#    return redirect('Producto:list')
#
#
#
#
#
#
#