from django import forms
from .models import ToDoItem, CustomUser
from django_flatpickr.widgets import DateTimePickerInput


class TaskForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'due_date', 'todo_list_employee']

        widgets = {
            'due_date': DateTimePickerInput(),
            'todo_list_employee': forms.widgets.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'due_date': "Крайний срок",
            'todo_list_employee': "Исполнитель"
        }

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.request.user.is_staff:
            self.fields['todo_list_employee'].queryset = CustomUser.objects.all()
        else:
            self.fields['todo_list_employee'].queryset = CustomUser.objects.filter(
                id=self.request.user.id)

    title = forms.CharField(label= 'Название', widget=forms.widgets.TextInput(attrs={'placeholder': 'Название', 'style': 'width: 300px;', 'class': 'form-control'}))
    description = forms.CharField(label= 'Описание',widget=forms.widgets.Textarea(attrs={'placeholder': 'Описание', 'style': 'width: 300px;', 'class': 'form-control', 'rows': '3'}))


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password','first_name', 'last_name', 'is_staff']

    username = forms.CharField(label= 'Логин',widget=forms.widgets.TextInput(attrs={'placeholder': 'логин', 'style': 'width: 300px;', 'class': 'form-control'}))
    password = forms.CharField(label= 'Пароль',widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Пароль', 'style': 'width: 300px;', 'class': 'form-control'}))
    first_name = forms.CharField(label= 'Имя',widget=forms.widgets.TextInput(attrs={'placeholder': 'Имя', 'style': 'width: 300px;', 'class': 'form-control'}))
    last_name = forms.CharField(label= 'Фамилия',widget=forms.widgets.TextInput(attrs={'placeholder': 'Фамилия', 'style': 'width: 300px;', 'class': 'form-control'}))
    is_staff = forms.BooleanField(label= 'Руководитель',required=False, widget=forms.widgets.CheckboxInput(attrs={}))
