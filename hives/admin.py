from django.contrib import admin
from .models import Hive, HiveActivity, ColonyHealthPrediction

admin.site.register(Hive)
admin.site.register(HiveActivity)
admin.site.register(ColonyHealthPrediction)
