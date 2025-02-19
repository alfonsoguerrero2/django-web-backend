from django.contrib import admin

# Register your models here.
from .models import Student, Professor, Module, Rating

# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Rating)





