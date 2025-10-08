from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    
    def __str__(self):
        return self.name
    

class CustomUsers(models.Model):
    login = models.CharField(max_length=25, verbose_name='Логин', unique=True)
    password_hash = models.CharField(max_length=150, verbose_name='Пароль')
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)
    surname = models.CharField(max_length=50,)
    email = models.EmailField(verbose_name='Мыло')
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, null=True)
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    

class UserProxy(CustomUsers):
    def set_password(self, raw_password: str):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password_hash)
    
    def has_perms(self, list_codes: list):
        role = get_object_or_404(Role.objects.prefetch_related('permissions'), id=self.role.id)
        role_perms = set(role.permissions.values_list('code', flat=True))
        required_perms = set(list_codes)
        return required_perms.issubset(role_perms)

    class Meta:
        proxy = True
    
