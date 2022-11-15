from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from ..classes.models import Classes

# Create your models here.


# class AmmenitySet(models.Model):
#     type = models.CharField(max_length=20, null=False)
#     quantity = models.PositiveIntegerField(
#         validators=[MaxValueValidator(9999)], null=False)

#     def __str__(self):
#         return str(self.type) + '  -  ' + str(self.quantity) + '  (' + str(self.id) + ')'

class Ammenity(models.Model):
    type = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.type)


class Image(models.Model):
    image = models.ImageField(upload_to='studios/images')

    def __str__(self):
        return str(self.image)


class Studio(models.Model):
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False)
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False)
    postal = models.CharField(max_length=7, null=False)
    phone_num = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)], null=False)
    images = models.ManyToManyField(
        Image, related_name='ImageSet', blank=True, through='ImageSet')
    ammenities = models.ManyToManyField(
        Ammenity, related_name='AmmenitySet', blank=True, through='AmmenitySet')
    # classes = models.ManyToManyField(Classes)

    def __str__(self):
        return str(self.name)


class AmmenitySet(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(Ammenity, on_delete=models.CASCADE, null=True)
    quanitity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.studio) + ': ' + str(self.type) + ' - ' + str(self.quanitity)

    class Meta:
        unique_together = [['studio', 'type']]


class ImageSet(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.studio) + ': ' + str(self.image)

    class Meta:
        unique_together = [['studio', 'image']]
