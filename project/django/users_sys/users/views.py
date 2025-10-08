from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView, ListView, DetailView

from .forms import AuthUserForm, RegUserForm, UserProfileForm, RoleForm
from .models import UserProxy, Role
from .mixins import PermissionRequiredMixin, AdminRequiredMixin

class AdminRolesListView(AdminRequiredMixin, ListView):
    template_name='users/list_roles.html'
    model = Role
    extra_context = {
        'title': 'Список ролей',
    }
    
    
class AdminRoleEditView(AdminRequiredMixin, View):
    template_name = 'users/edit_role.html'
    
    def get(self, request, name_role):
        role = get_object_or_404(Role.objects.prefetch_related('permissions'), name=name_role)
        form = RoleForm(instance=role)
        return render(request, self.template_name, {'form': form, 'title': name_role})
    
    def post(self, request, name_role):
        role = get_object_or_404(Role, name=name_role)
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('users:list-roles')
        return render(request, self.template_name, {'form': form, 'title': name_role})
 
    
class DeleteRoleView(AdminRequiredMixin, View):
    def post(self, request, name_role):
        obj = get_object_or_404(Role, name=name_role)
        obj.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class UserDeleteView(PermissionRequiredMixin, View):
    permission_required = ['delete_user']
    
    def post(self, request):
        obj = get_object_or_404(UserProxy, id=request.user.id)
        obj.is_active = False
        obj.save()
        
        return redirect('users:logout')

    
class UserLogoutView(View):
    def get(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
        request.user = None
        return redirect('users:login')


class UserLoginView(FormView):
    form_class = AuthUserForm
    template_name = 'users/login.html'

    extra_context = {
        'title': 'Авторизация'
    }
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('users:profile'))
        return super().get(request)
    
    def form_valid(self, form):
        user = form.cleaned_data['user']
        self.request.session['user_id'] = user.id
        return redirect(reverse_lazy('users:profile'))


class UserRegView(CreateView):
    model = UserProxy
    form_class = RegUserForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('users:login')

    extra_context = {
        'title': 'Регистрация'
    }


class UserProfileView(UpdateView):
    model = UserProxy
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy('users:profile')

    extra_context = {
        'title': 'Редактирование профиля'
    }

    def get_object(self):
        return self.request.user
