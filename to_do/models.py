from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

def one_week_since_now():
    return timezone.now() + timezone.timedelta(days=7)


class ToDoItem(models.Model): #класс задачи
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_since_now)
    todo_list_employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)





