from django import forms
from django.contrib.auth.models import User
from .models import UserDetails
from .models import Book
from .models import Review

# Formulario de inicio de sesión
class LoginForm(forms.Form):
   username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Formulario para editar información básica del usuario
class UserEditForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['username', 'first_name', 'last_name', 'email']

# Formulario para editar detalles adicionales del usuario
class UserDetailsForm(forms.ModelForm):
   class Meta:
       model = UserDetails
       fields = ['rol', 'fecha_nacimiento', 'fono', 'numero_doc', 'dv', 'pasaporte']

# Formulario combinado que incluye campos de User y UserDetails
class CombinedUserEditForm(UserEditForm):
   class Meta(UserEditForm.Meta):
       model = User
       fields = UserEditForm.Meta.fields + ['userdetails']

   userdetails = forms.ModelChoiceField(queryset=UserDetails.objects.all(), widget=forms.HiddenInput())

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['userdetails'].queryset = UserDetails.objects.filter(user=self.instance)
       if self.instance and hasattr(self.instance, 'userdetails'):
           self.fields['userdetails'].initial = self.instance.userdetails

# Formulario de registro
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # Validación para confirmar que ambas contraseñas coinciden
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'isbn']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }