# organizations/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Organization, Role

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address', 'is_main']

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'organization', 'role']

class RoleAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ModelChoiceField(queryset=Role.objects.all())

class UserRegistrationForm(UserCreationForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True,
        empty_label="Select Organization"
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=True,
        empty_label="Select Role"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'organization', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field attributes if necessary
        self.fields['organization'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})

class AssignRoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name'] 
        labels = {
            'name': 'Role',  
        }
