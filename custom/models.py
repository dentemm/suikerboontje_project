from django.db import models

# Create your models here.

class CustomImage(models.Model):

	image = models.ImageField(upload_to='images/presentions/')
	caption = models.CharField(max_length=256, null=True, blank=True)
