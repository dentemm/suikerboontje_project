from django.core.management.base import BaseCommand, CommandError

#from oscar.apps.catalogue.abstract_models import AbstractProduct
from custom.models import CustomImage, ThumbnailImage

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'Maak thumbnails aan voor alle CustomImage objecten'

		for image in CustomImage.objects.all():

			new, created = ThumbnailImage.objects.get_or_create(image=image.image)

			if created:
				new.save()
				print('creating new!')

		self.stdout.write('--Het is gefixt!--')




