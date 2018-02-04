from django.db import models

# Create your models here.

class Test(models.Model):
    pass

class Person(models.Model):
    name = models.CharField(max_length=20)
    birth = models.DateTimeField()