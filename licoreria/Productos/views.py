from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Producto,Tipo,Venta,DetalleVenta
from .forms import FormProducto,FiltrosProducto,FormExistencia,FiltrosVenta,FiltrosDetalleVenta,DetalleVentaForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from Proveedores.decorators import GroupRequiredMixin,group_required

class ListaProductos(LoginRequiredMixin,GroupRequiredMixin,ListView):
    group_required='Empleado'
    model=Producto
    paginate_by=6
    extra_context = {'form': FiltrosProducto}

class NuevoProducto(LoginRequiredMixin,GroupRequiredMixin,CreateView):
    group_required='Owner'
    model = Producto
    form_class = FormProducto
    # fields = '_all_'
    success_url = reverse_lazy('Producto:lista_productos')
    extra_context = {'accion': 'Nueva'}

@group_required('Owner')
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

@group_required('Owner')
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



@group_required('Owner')    
def eliminar_producto(request, clave):
    Producto.objects.get(clave=clave).delete()
    return redirect('Producto:lista_productos')

class Bienvenido(TemplateView):
    template_name = 'home.html'

@group_required('Empleado')
def buscar_materia(request):
    productos = Producto.objects.all().order_by('-clave')
    
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
        
    paginator = Paginator(productos, 6)  # Show 25 contacts per page.
    page_number = request.POST.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'form': form
    } 
    
    return render(request, 'Productos/producto_list.html', context)

@group_required('Owner')
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

@group_required('Empleado')
def busca_tipos(request):
    id_categoria=request.POST.get('id_categoria',None)
    if id_categoria:
        tipos=Tipo.objects.filter(categoria_id=id_categoria)
        data = [{'id':tipo.id,'nombre':tipo.nombre} for tipo in tipos]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error':'Parametro invalido'},safe=False)

@group_required('Empleado')
def create_venta(request):
    user = request.user

    # Check if there is an existing Venta without any DetalleVenta
    existing_venta = Venta.objects.filter(usuario=user, detalleventa__isnull=True).last()

    if existing_venta:
        venta = existing_venta
    else:
        # Create a new Venta object with the current date
        venta = Venta(usuario=user)
        venta.save()

    venta_pk = venta.pk
    return redirect('Producto:detalle_venta_create')

@group_required('Empleado')
def detalle_venta_list(request):
    detalle_venta = DetalleVenta.objects.all()
    return render(request, 'detalle_venta/list.html', {'detalle_venta': detalle_venta})


class ListaDetalleVenta(ListView):
    group_required='Empleado'
    model = DetalleVenta
    template_name = 'detalle_venta/list.html'
    context_object_name = 'detalle_venta'
    paginate_by=10
    extra_context = {'form': FiltrosDetalleVenta}


@group_required('Empleado')
def detalle_venta_create(request):
    message = None  # Initialize the message variable
    
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            detalle_venta = form.save(commit=False)
            last_venta = Venta.objects.last()
            producto = detalle_venta.producto
            existencia = producto.existencia - detalle_venta.cantidad
            
            if existencia < 0:
                # Set the message variable
                
                return render(request, 'detalle_venta/Insuficiente.html')
            
            producto.existencia = existencia
            producto.save()
            detalle_venta.id_venta = last_venta
            detalle_venta.save()
            return redirect('Producto:buscar_venta')
    else:
        form = DetalleVentaForm()
        
    return render(request, 'detalle_venta/create.html', {'form': form, 'message': message})



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

@group_required('Owner')
def detalle_venta_delete(request, pk):
    detalle_venta = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'POST':
        detalle_venta.delete()
        return redirect('detalle_venta_list')
    return render(request, 'detalle_venta/delete.html', {'detalle_venta': detalle_venta})

@group_required('Empleado')
def detalle_venta_view(request, id_venta):
    detalle_ventas = DetalleVenta.objects.filter(id_venta=id_venta)

    return render(request, 'detalle_venta.html', {'detalle_ventas': detalle_ventas})

@group_required('Empleado')
def buscar_detalleventa(request):
    ventas = DetalleVenta.objects.all().order_by('-id_venta')
    
    if request.method == 'POST':
        form = FiltrosDetalleVenta(request.POST)
        # Retrieve filter parameters from the request
        # Adjust the field names as per your form fields
        id_venta = request.POST.get('id_venta', None)

        if id_venta:
            ventas = ventas.filter(id_venta)

        print(ventas.query)
    else:
        form = FiltrosDetalleVenta()
    
    paginator = Paginator(ventas, 10)  # Show 5 ventas per page.
    page_number = request.POST.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'form': form
    } 
    
    return render(request, 'Productos/detalleventa_list.html', context)

@group_required('Owner')
def eliminar_todas_ventas(request):
    variable_names = list(request.POST.keys())
    if len(variable_names) != 0:
        variable_names.pop(0)
        if len(variable_names) != 0:
            for id_venta in variable_names:
                try:
                    venta = Venta.objects.get(pk=id_venta)
                    detalles_venta = DetalleVenta.objects.filter(id_venta=venta)
                    for detalle_venta in detalles_venta:
                        producto = detalle_venta.producto
                        existencia = producto.existencia + detalle_venta.cantidad
                        producto.existencia = existencia
                        producto.save()
                    venta.delete()
                except Venta.DoesNotExist:
                    pass
    return redirect('Producto:buscar_venta')



#def eliminar_todas(request):
#    variable_names = list(request.POST.keys())
#    if(len(variable_names)!=0):
#        variable_names.pop(0)
#        #print(variable_names)
#        #print(dict[request.POST])
#        if(len(variable_names)!=0):
#            for clave in variable_names:
#                Producto.objects.get(clave=clave).delete()
#    return redirect('Producto:lista_productos')