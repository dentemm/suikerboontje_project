from django.db import models

from sorl.thumbnail import ImageField

# Create your models here.

class CustomImage(models.Model):

	image = models.ImageField(upload_to='images/presentions/')
	caption = models.CharField(max_length=256, null=True, blank=True)


	class Meta:
		ordering = ['image', ]

	def __str__(self):
		return self.image


class ThumbnailImage(models.Model):

	image = ImageField(upload_to='images/presentations/thumbnails/')

	class Meta:
		ordering = ['image', ]

	def __str__(self):
		return str(self.image)
