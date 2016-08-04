from django.core.management.base import BaseCommand, CommandError

#from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.catalogue.models import Product, ProductAttribute

class Command(BaseCommand):

	def handle(self, *args, **options):

		help = 'Voorziet alle voedingsproducten van 6 procent BTW'

		for product in Product.objects.all():

			if product.product_class.name == 'Voedingswaren 6%':

				print 'voeding!'

				for attribute in product.attributes.all():

					if attribute.name == 'BTW':

						print 'tis BTW'
						print attribute.type

						if attribute.type == 'option':

							print attribute.option_group

							print attribute.option_group.options.count()

						attribute.type = 'option'
						attribute.save()

		self.stdout.write('--Het is gefixt!--')




