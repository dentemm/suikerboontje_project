from django.contrib import admin

# Register your models here.
from .models import CustomImage, ThumbnailImage

@admin.register(CustomImage)
class CustimImageAdmin(admin.ModelAdmin):
	pass

@admin.register(ThumbnailImage)
class ThumbnailImageAdmin(admin.ModelAdmin):
	pass

