from django.contrib import admin
from .models import Studio, AmmenitySet, Ammenity, ImageSet, Image

# Register your models here.


class ammenitiesInline(admin.TabularInline):
    model = Studio.ammenities.through


class imagesInLine(admin.TabularInline):
    model = Studio.images.through


class StudioAdmin(admin.ModelAdmin):
    # list_display = ['name', 'address', 'latitude',
    #                 'longitude', 'postal', 'phone_num', 'images', 'get_ammenities']
    # list_display_links = ['name']

    # def get_ammenities(self, obj):
    #     if obj.ammenities.all():
    #         return list(obj.ammenitites.all().values_list('a', flat=True))
    inlines = [ammenitiesInline, imagesInLine]

    class Meta:
        model = Studio


admin.site.register(Studio, StudioAdmin)
admin.site.register(AmmenitySet)
admin.site.register(Ammenity)
admin.site.register(ImageSet)
admin.site.register(Image)
