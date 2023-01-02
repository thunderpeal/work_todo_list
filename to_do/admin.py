from django.contrib import admin

# Register your models here.
from django.contrib import admin
from to_do.models import ToDoItem
from to_do.models import CustomUser

admin.site.register(ToDoItem)
admin.site.register(CustomUser)