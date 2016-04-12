from django.contrib import admin
from .models import Process, ProcessChild
# Register your models here.
admin.site.register(Process)
admin.site.register(ProcessChild)