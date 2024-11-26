from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View, UpdateView
from django.shortcuts import get_object_or_404, redirect
from .models import Organization, CustomUser, Role
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from .forms import AssignRoleForm, UserRegistrationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, 'Login successful!')
            return redirect(reverse('home_page'))  # Redirect to the home page after login
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'registration/login.html')  # Render the login form

def home_page(request):
    return render(request, 'home.html')

class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/organization_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Organization.objects.all()
        return Organization.objects.filter(users=self.request.user)

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name', 'address']
    template_name = 'organization/organization_form.html'
    success_url = reverse_lazy('organization-list')

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            messages.error(request, "Only superusers can create organizations.")
            return redirect('organization-list')  # Redirect to the organization list or another page
        return super().dispatch(request, *args, **kwargs)


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all users associated with the organization
        context['users'] = CustomUser.objects.filter(organization=self.object)
        return context


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.user.organization:
            return CustomUser.objects.filter(organization=self.request.user.organization)
        return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = self.request.user.organization
        context['organization'] = organization
        return context


class AssignRoleView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = AssignRoleForm()
        return render(request, 'users/assign_role.html', {'form': form, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['name']  # Get the selected role
            user.role = role  # Assign the role to the user
            user.save()
            return redirect('user-list')  # Redirect to the user list page
        return render(request, 'users/assign_role.html', {'form': form, 'user': user})


@login_required
def add_user(request, organization_id):
    # Fetch the organization
    organization = get_object_or_404(Organization, id=organization_id)

    # Restrict superuser from adding users
    if request.user.is_superuser:
        messages.error(request, "Superusers cannot add users.")
        return redirect('organization-list')

    # Check if the user is the admin of the organization
    if request.user.role.name != 'admin':
        messages.error(request, "You are not authorized to add users to this organization.")
        return redirect('organization-detail', pk=organization_id)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = organization
            user.save()
            messages.success(request, f"User '{user.username}' added successfully!")
            return redirect('organization-detail', pk=organization.id)
        else:
            messages.error(request, "There was an error adding the user. Please check the form.")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/user_add.html', {'form': form, 'organization': organization})



def logoutView(request):
    messages.success(request, 'Logout successful!')
    return redirect('login')


@login_required
def update_user(request, user_id):
    # Fetch the user to update
    user = get_object_or_404(CustomUser, id=user_id)

    # Prevent superusers from updating user details
    if request.user.is_superuser:
        messages.error(request, "Superusers cannot update user details.")
        return redirect('organization-list')

    # Allow only the organization's admin to update the user's role
    if request.method == 'POST':
        if request.user.role.name == 'admin':
            role_id = request.POST.get('role')  # Get the role ID from the form
            if role_id:
                try:
                    # Fetch the Role instance
                    role = Role.objects.get(id=role_id)
                    user.role = role  # Set the role
                    user.save()  # Save the updated user
                    messages.success(request, f"Role for user '{user.username}' updated successfully!")
                except Role.DoesNotExist:
                    messages.error(request, "Invalid role selected.")
            else:
                messages.error(request, "Please provide a valid role.")
        else:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('organization-list')

        return redirect('organization-detail', pk=user.organization.id)

    # Prepare the data for rendering
    role = Role.objects.all()
    context = {'user': user, 'all_role': role }
    return render(request, 'users/user_update.html', context)


@login_required
def delete_user(request, user_id):
    # Fetch the user to delete
    user = get_object_or_404(CustomUser, id=user_id)

    # Prevent superusers from deleting users
    if request.user.is_superuser:
        messages.error(request, "Superusers cannot delete users.")
        return redirect('organization-list')

    # Allow only the organization's admin to delete users
    if request.user.role.name != 'admin':
        messages.error(request, "You are not authorized to delete this user.")
        return redirect('organization-list')

    user.delete()
    messages.success(request, f"User '{user.username}' deleted successfully!")
    return redirect('organization-detail', pk=user.organization.id)


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'users/user_add.html'
    fields = ['username', 'email', 'password', 'role']
    success_url = '/org/users/'  # Redirect to the user list page after creation


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'address']
    template_name = 'organization/organization_form.html'
    success_url = reverse_lazy('organization-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        # Allow only superusers to update organizations
        if not request.user.is_superuser:
            messages.error(request, "Only superusers can update organizations.")
            return redirect('organization-list')
        return super().dispatch(request, *args, **kwargs)


@login_required
def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)

    # Allow only superusers to delete organizations
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can delete organizations.")
        return redirect('organization-list')

    organization.delete()
    messages.success(request, f"Organization '{organization.name}' deleted successfully!")
    return redirect('organization-list')


@login_required
def assign_admin(request, organization_id, user_id):
    # Ensure the user is a superuser to perform this action
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('organization-list')

    # Fetch the organization and user
    organization = get_object_or_404(Organization, id=organization_id)
    user = get_object_or_404(CustomUser, id=user_id)

    # Check if the user belongs to the same organization
    if user.organization != organization:
        messages.error(request, "User does not belong to this organization.")
        return redirect('organization-detail', pk=organization_id)

    # Assign the user as the admin
    organization.admin = user
    organization.save()

    messages.success(request, f"{user.username} has been assigned as the admin for {organization.name}.")
    return redirect('organization-detail', pk=organization_id)