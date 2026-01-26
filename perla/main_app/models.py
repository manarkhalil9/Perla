from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
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

# vision model
class Vision(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True)
    target_month = models.CharField(max_length=3, choices=MONTHS)
    image = models.ImageField(upload_to='main_app/static/uploads/', default='', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.get_target_month_display()}'
    
    def get_absolute_url(self):
        return reverse('vision_detail', kwargs={'pk': self.id})
    
# visions tasks model
class VisionTask(models.Model):
    title = models.CharField(max_length=100)
    month = models.CharField(max_length=3, choices=MONTHS)
    vision = models.ForeignKey(Vision, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.get_month_display()}'
    
    def get_absolute_url(self):
        return reverse('vision_detail', kwargs={'vision_id': self.vision.id})

# todoItem model
class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    priority = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
