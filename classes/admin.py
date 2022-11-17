from django.contrib import admin
from classes.models import Class, Classes, Keyword

# Register your models here.
admin.site.register(Classes)
admin.site.register(Class)
admin.site.register(Keyword)
