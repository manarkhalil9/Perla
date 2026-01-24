from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

# vision model
class Vision(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_month = models.IntegerField()
    image = models.ImageField(upload_to='main_app/static/uploads/', default='')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('vision_detail', kwargs={'vision_id': self.id})
    
# visions tasks model
MONTHS = (
    ('JAN', 'January'),
    ('FEB', 'February'),
    ('MAR', 'March'),
    ('APR', 'April'),
    ('MAY', 'May'),
    ('JUN', 'June'),
    ('JUL', 'July'),
    ('AUG', 'August'),
    ('SEP', 'September'),
    ('OCT', 'October'),
    ('NOV', 'November'),
    ('DEC', 'December'),
)

class VisionTask(models.Model):
    title = models.CharField(max_length=100)
    month = models.CharField(max_length=3, choices=MONTHS)
    vision = models.ForeignKey(Vision, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.get_month_display()})"


# todoItem model
class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    priority = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
