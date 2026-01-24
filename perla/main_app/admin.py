from django.contrib import admin
from .models import Vision, VisionTask, TodoItem

# Register your models here.
admin.site.register(Vision)
admin.site.register(VisionTask)
admin.site.register(TodoItem)