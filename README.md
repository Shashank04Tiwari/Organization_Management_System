# Organization_Management_System
This project is a Django web application designed to manage users and organizations. It includes functionalities for user authentication, user roles management, and organization management. Users can belong to multiple organizations, and each organization can have a designated admin. Superusers have the highest level of access, while organization admins can manage users within their organizations.

->Project Structure:
*Views: All the views in the project are built using Django's class-based views (CBVs) and function-based views (FBVs).

->Function-Based Views (FBVs):
login_view: Handles user login functionality.
home_page: Displays the home page.
add_user: Allows an admin user to add new users to an organization.
logoutView: Logs out a user and redirects to the login page.
update_user: Allows an admin to update a user's role within the organization.
delete_user: Allows an admin to delete a user from the organization.
delete_organization: Allows superusers to delete organizations.
assign_admin: Allows superusers to assign an organization admin.

->Class-Based Views (CBVs):
OrganizationListView: Displays a list of organizations. Available to all authenticated users, but restricted to the user's organization.
OrganizationCreateView: Allows superusers to create new organizations.
OrganizationDetailView: Displays detailed information about an organization, including users.
UserListView: Lists users of an organization.
AssignRoleView: Allows the admin to assign roles to users.
OrganizationUpdateView: Allows superusers to update organizations.

->Models:

Organization: Represents an organization. An organization can have many users, and each organization can have an admin.
CustomUser: Represents the user model, extended from Django’s default User model. Each user has a role (admin, member, etc.) and is assigned to an organization.
Role: Represents the different roles a user can have within an organization (e.g., admin, member).
Forms:

->AssignRoleForm: A form used to assign roles to users.
UserRegistrationForm: A form for registering new users, including input fields for username, email, password, and role.

->URLs:
Defined in the urls.py to route to the appropriate views, such as organization-list, organization-create, user-list, etc.

-> Templates:
The project utilizes several HTML templates to render the user interface. These templates are responsible for displaying forms, lists, and details for organizations and users, and ensuring that the user interface is consistent and user-friendly. Below is a summary of the templates used in the view.


**Instructions on setting up and running the project locally**

1. Create virtual env if the current one is not working and activate it.
2. Install Django(pip install django).
3. Run the server(python manage.py runserver).
4. Open the browser and navigate to http://127.0.0.1:8000
5. Credentials ->
* Superuser - username - shashank, password - shashank
* company admin(Bombay Softwares) - username - laiba, password - 12345@LS
* company admin(Vasundhara) - username - shashankv, password - 12345@ST
