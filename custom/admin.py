from django.contrib import admin

# Register your models here.
from .models import CustomImage

@admin.register(CustomImage)
class CustimImageAdmin(admin.ModelAdmin):
	pass
