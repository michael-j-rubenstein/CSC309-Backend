from django.contrib import admin
from classes.models import Class, Classes, Keyword


class ClassesAdmin(admin.ModelAdmin):

    def post_save(self, instance):
        instance.create_edit_class()

# Register your models here.
admin.site.register(Class)
admin.site.register(Keyword)
admin.site.register(Classes, ClassesAdmin)

