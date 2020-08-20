from django.contrib import admin

# Register your models here.

from .models import Challenger, Exercise, Column

admin.site.register(Challenger)
admin.site.register(Exercise)
admin.site.register(Column)
