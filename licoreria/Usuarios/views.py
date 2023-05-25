from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from .forms import FormUsuariosLicoreria,FiltrosUsuario
from django.views.generic import DeleteView
from django.contrib.auth.models import User, Group
from Proveedores.decorators import GroupRequiredMixin,group_required

from django.contrib.auth.mixins import LoginRequiredMixin
class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


class ListaUsuarios(LoginRequiredMixin,GroupRequiredMixin,ListView):
    group_required='Owner'
    model=User
    paginate_by=10
    template_name = 'lista_usuarios.html'
    extra_context = {'form': FiltrosUsuario}

@group_required('Owner')
def lista_usuarios(request):
    usuarios = User.objects.all()
    grupos = Group.objects.all()
    
    
    context = {
        'usuarios': usuarios,
        'grupos': grupos
    }
    
    return render(request, 'lista_usuarios.html', context)

@group_required('Owner')
def crear_usuario(request):
    if request.method == 'POST':
        form = FormUsuariosLicoreria(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = FormUsuariosLicoreria()
    return render(request, 'usuario_form.html', {'form': form})

@group_required('Owner')
def editar_usuario(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormUsuariosLicoreria(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = FormUsuariosLicoreria(instance=user)
    return render(request, 'usuario_form.html', {'form': form})

@group_required('Owner')
def eliminar_usuario(request, id):
    user = get_object_or_404(User, id=id)
    usuario_licoreria = user.usuarioslicoreria
    if usuario_licoreria:
        usuario_licoreria.delete()
    user.delete()
    return redirect('lista_usuarios')

class EliminarUsuario(LoginRequiredMixin,GroupRequiredMixin,DeleteView):
    group_required='Owner'
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('lista_usuarios')


@group_required('Owner')
def asignar_grupo(request):
    #print(dict[request.POST])
    variable_names=list(request.POST.keys())
    grupo=request.POST.get('grupo')
    group=Group.objects.get(id=grupo)
    if(len(variable_names)!=0):
        variable_names.pop(0)
        if(len(variable_names)!=0):
            for x in variable_names[:-1]:
                group.user_set.add(x)

    return redirect('lista_usuarios')

@group_required('Owner')
def remove_user_groups(request, pk):
    user = User.objects.get(id=pk)
    user.groups.clear()
    return redirect('lista_usuarios')