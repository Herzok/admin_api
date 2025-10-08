from django.http import HttpResponseForbidden

class PermissionRequiredMixin:
    """
    Миксин для CBV, проверяет, есть ли у пользователя нужное право.
    """
    permission_required = None  # код права, например 'delete_post'

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required is None:
            raise ValueError("Укажите permission_required для этого view")
        
        if not request.user.has_perms(self.permission_required):
            return HttpResponseForbidden("У вас нет доступа")

        return super().dispatch(request, *args, **kwargs)
    
class AdminRequiredMixin:
    """Доступ только для пользователей с ролью 'admin'."""
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role.name not in ['admin', 'superuser'] :
            return HttpResponseForbidden("Доступ запрещён: требуются права администратора.")
        return super().dispatch(request, *args, **kwargs)