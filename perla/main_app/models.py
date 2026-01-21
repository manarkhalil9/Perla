from django.db import models

# Create your models here.
class Vision(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_month = models.CharField(max_length=20)

    def __str__(self):
        return self.name