
from django.urls import path
from .views import *
from organizations import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('home_page/', views.home_page, name = 'home_page'),
    path('', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('org/<int:pk>/update/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('org/<int:organization_id>/delete/', delete_organization, name='organization-delete'),
    path('org/organizations/<int:pk>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/add/<int:organization_id>/', views.add_user, name='user-add'),  
    path('users/<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('logout/', views.logoutView, name='logout'),
    path('<int:user_id>/update/', update_user, name='user-update'),
    path('<int:user_id>/delete/', delete_user, name='user-delete'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('organization/<int:organization_id>/assign-admin/<int:user_id>/', views.assign_admin, name='assign-admin'),
]
