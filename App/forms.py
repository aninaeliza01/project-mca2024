from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail Address')
    phone = forms.CharField(max_length=12, required=True, label='Phone Number')
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, label='Role')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['password1'].help_text = 'Your password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
