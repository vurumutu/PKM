from django.contrib import admin
from .models import TrainRequest
from .models import AvailableTrain

admin.site.register(TrainRequest)
admin.site.register(AvailableTrain)
# Register your models here.
