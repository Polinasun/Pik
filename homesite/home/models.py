from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Homes(models.Model):

    address = models.CharField(max_length = 30)
    number_bricks=models.IntegerField(default = 0)
    year=models.IntegerField(validators=[MinValueValidator(1900),MaxValueValidator(2020)])
    uuid = models.UUIDField(primary_key = True, default = uuid4)


    def __str__(self):
        return self.title

class Bricks(models.Model):
    
    number=models.IntegerField()
    uuid = models.UUIDField(primary_key = True, default = uuid4)


    def __str__(self):
        return self.title