
from django import forms
from .models import UserProxy,Role, Permission

class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Права доступа"
    )

    class Meta:
        model = Role
        fields = ['permissions']

class RegUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput({'placeholder': "Введи пароль"}), label='Новый пароль')
    password2 = forms.CharField(widget=forms.PasswordInput({'placeholder': "Повтори пароль"}), label='Повторить пароль')
    first_name = forms.CharField(widget=forms.TextInput(attrs=({'placeholder': 'Введи имя'})), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs=({'placeholder': 'Введи фамилию'})), label='Фамилия')
    login = forms.CharField(widget=forms.TextInput(attrs=({'placeholder': 'Введи логин'})), label='Логин')
    email = forms.CharField(widget=forms.EmailInput(attrs=({'placeholder': 'Введи мыло'})), label='Email')
    
    class Meta:
        model = UserProxy
        fields = ['login', 'first_name', 'last_name', 'email']
        
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = Role.objects.get(id=2)
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProxy.objects.filter(email=email).exists():
            raise forms.ValidationError('Такое мыло уже есть!')
        return email
    
class AuthUserForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введи логин'}), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введи пароль'}), label='Пароль')
        
    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if login and password:
            try:
                user = UserProxy.objects.get(login=login, is_active=True)
            except UserProxy.DoesNotExist:
                raise forms.ValidationError("Пользователь не найден")

            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")

            cleaned_data["user"] = user

        return cleaned_data
        
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(), label='Фамилия')
    login = forms.CharField(widget=forms.TextInput(attrs={"readonly": True}), label='Логин')
    email = forms.CharField(widget=forms.TextInput(attrs={"readonly": True}), label='Email')

    class Meta:
        model = UserProxy
        fields = ['first_name', 'last_name', 'login', 'email']
