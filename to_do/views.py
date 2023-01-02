from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password

from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import TaskForm, UserCreateForm
from to_do.models import CustomUser, ToDoItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class MainListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "to_do/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = ToDoItem.objects.all().order_by('due_date')
        context['curr_page'] = 'Главная'
        context['tasks_total'] = len(ToDoItem.objects.filter(Q(done=False)))
        return context


class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = "to_do/employees.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = CustomUser.objects.filter(Q(is_staff=False))
        context['employees'] = employees
        context['curr_page'] = 'Сотрудники'
        context['annotation'] = 'Всего сотрудников: ' + str(len(employees))
        return context

    def test_func(self):
        return self.request.user.is_staff


class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'to_do/employees_create.html'
    success_url = reverse_lazy('employees')

    def form_valid(self, form):
        user = form.save()
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super(EmployeeCreate, self).form_valid(form)


class EmployeeChange(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'to_do/employees_change.html'
    success_url = reverse_lazy('employees')

    def form_valid(self, form):
        user = form.save()
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super(EmployeeChange, self).form_valid(form)


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'to_do/employee_delete.html'
    success_url = reverse_lazy('employees')


class TasksPerE(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "to_do/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = int(str(self.request).split('/')[-1][:-2])
        user = CustomUser.objects.filter(id=user_id)[0]
        tasks = ToDoItem.objects.filter((Q(todo_list_employee=user_id) & Q(done=False))).order_by('due_date')
        context['tasks'] = tasks
        context['curr_page'] = 'Задачи'
        context['person'] = 'Сотрудник: ' + user.first_name + ' ' + user.last_name
        context['annotation'] = 'Всего задач: ' + str(len(tasks))
        return context


class ArchivePerE(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "to_do/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = int(str(self.request).split('/')[-1][:-2])
        user = CustomUser.objects.filter(id=user_id)[0]
        tasks = ToDoItem.objects.filter((Q(todo_list_employee=user_id) & Q(done=True))).order_by('-due_date')
        context['tasks'] = tasks
        context['person'] = 'Сотрудник: ' + user.first_name + ' ' + user.last_name
        context['annotation'] = 'Задач в архиве: ' + str(len(tasks))
        context['curr_page'] = 'Архив'
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'to_do/task_create.html'

    def get_success_url(self):
        return reverse_lazy('tasks_per_e', args=[self.request.user.id])

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class TaskChange(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    form_class = TaskForm
    template_name = 'to_do/task_change.html'

    def get_success_url(self):
        return reverse_lazy('tasks_per_e', args=[self.request.user.id])

    def get_form_kwargs(self):
        kwargs = super(TaskChange, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem
    template_name = 'to_do/task_delete.html'
    where = 'tasks'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('main')
        return reverse_lazy('tasks_per_e', args=[self.request.user.id])


class Calendar(LoginRequiredMixin, ListView):
    ordering = 'due_date'
    model = ToDoItem
    template_name = "to_do/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            items = ToDoItem.objects.all().order_by('due_date')
        else:
            items = ToDoItem.objects.filter(Q(todo_list_employee=self.request.user)).order_by('due_date')
        context['items'] = items
        context['curr_page'] = 'Календарь'
        return context


class CustomSignInView(LoginView):
    template_name = 'to_do/login.html'
    fields = ['username', 'password']
    success_url = reverse_lazy('main')

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('main')
        return reverse_lazy('tasks_per_e', args=[self.request.user.id])


class CustomSignOutView(LogoutView):
    next_page = reverse_lazy('login')


def set_task_done(request, pk):
    cur_task = ToDoItem.objects.filter(id=pk)[0]
    new_val = not cur_task.done
    cur_task.done = new_val
    cur_task.save()
    where = 'archive'
    if new_val:
        where = 'tasks'
    if request.user.is_staff:
        where = 'employees'
    return redirect(reverse_lazy(where))
