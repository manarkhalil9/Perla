from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from cloudinary.models import CloudinaryField

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
    description = models.TextField(blank=True, null=True)
    target_month = models.CharField(max_length=3, choices=MONTHS)
    image = CloudinaryField('image', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.get_target_month_display()}'
    
    # this method runs during form validation
    def clean(self):
        super().clean()
        # if both fields are missing, the data is invalid
        if not self.description and not self.image:
            raise ValidationError('You must provide either a description or an image.')
        
    # overriding save ensures the clean() logic is enforced even outside of forms
    def save(self, *args, **kwargs):
        # manually trigger the clean() method
        self.full_clean() 
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('vision_detail', kwargs={'vision_id': self.id})
    
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
    date = models.DateField(default=date.today)
    priority = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(VisionTask, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
