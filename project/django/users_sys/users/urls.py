from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'users'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('reg', UserRegView.as_view(), name='reg'),
    path('profile', login_required(UserProfileView.as_view()), name='profile'),
    path('logout',  login_required(UserLogoutView.as_view()), name='logout'),
    path('delete', login_required(UserDeleteView.as_view()), name='delete'),
    path('roles/', login_required(AdminRolesListView.as_view()), name='list-roles'),
    #path('roles/create', login_required(.as_view()), name='create-role'),
    path('roles/delete/<str:name_role>', login_required(DeleteRoleView.as_view()), name='delete-role'),
    path('roles/edit/<str:name_role>', login_required(AdminRoleEditView.as_view()), name='edit-role'),
]