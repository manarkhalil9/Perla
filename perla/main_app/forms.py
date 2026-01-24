from django.forms import ModelForm
from .models import VisionTask

class VisionTaskForm(ModelForm):
    class Meta:
        model = VisionTask
        fields = ['title', 'month']
