from django.urls import path
from .views import EmployeeListView, MainListView, EmployeeCreate, EmployeeChange, EmployeeDelete, \
    TaskCreate, TaskChange, TaskDelete, Calendar, CustomSignInView, CustomSignOutView, \
    set_task_done, TasksPerE, ArchivePerE


urlpatterns = [
    path("", MainListView.as_view(), name='empty'),
    path("to_do", MainListView.as_view(), name='main'),
    path("to_do/employees", EmployeeListView.as_view(), name="employees"),
    path("to_do/employees_create", EmployeeCreate.as_view(), name="employee_create"),
    path("to_do/employees_change/<int:pk>/", EmployeeChange.as_view(), name="employee_change"),
    path("to_do/employee_delete/<int:pk>/", EmployeeDelete.as_view(), name="employee_delete"),
    path("to_do/set_done/<int:pk>/", set_task_done, name="set_done"),
    path("to_do/tasks_per_e/<int:pk>", TasksPerE.as_view(), name="tasks_per_e"),
    path("to_do/archive_per_e/<int:pk>", ArchivePerE.as_view(), name="archive_per_e"),
    path("to_do/task_change/<int:pk>/", TaskChange.as_view(), name="task_change"),
    path("to_do/task_create", TaskCreate.as_view(), name="task_create"),
    path("to_do/task_delete/<int:pk>/", TaskDelete.as_view(), name="task_delete"),
    path("to_do/calendar", Calendar.as_view(), name="calendar"),
    path("accounts/login/", CustomSignInView.as_view(), name="login"),
    path("accounts/logout/", CustomSignOutView.as_view(), name="logout"),
]
