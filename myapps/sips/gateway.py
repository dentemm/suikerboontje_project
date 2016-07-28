# -*- coding: utf-8 -*-

import hmac 
import hashlib
import base64
import collections
import json
import requests
from Crypto.Hash import HMAC, SHA256

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


from oscar.apps.payment.exceptions import GatewayError, UnableToTakePayment

#from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment


# SIPS JSON PAYPAGE
SIPS_PAYPAGE_TEST_HOST = 'payment-webinit.simu.sips-atos.com'
SIPS_PAYPAGE_LIVE_HOST = 'payment-webinit.sips-atos.com'
SIPS_PAYPAGE_PATH = '/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_URL = 'https://payment-webinit.simu.sips-atos.com/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_URL_PRODUCTION = 'https://payment-webinit.sips-atos.com/rs-services/v2/paymentInit/'
SIPS_PAYPAGE_SECRET_KEY = '002001000000001_KEY1'
SIPS_PAYPAGE_MERCHANT = '002001000000001'


SIPS_PATH = '/rs-services/v2/paymentInit'
SIPS_MERCHANT = '002001000000001'
SIPS_PASSWORD = '002001000000001_KEY1'	# secret key
SIPS_KEY_VERSION = '1'
SIPS_ORDER_CHANNEL = 'INTERNET'
SIPS_INTERFACE_VERSION = 'IR_WS_2.10'
SIPS_CURRENCY_CODE = '978'
SIPS_PAYMENT_MEAN_BRAND = 'BCMC'
SIPS_PAYMENT_MEAN_TYPE = 'CARD'

# SIPS OFFICE JSON 
SIPS_OFFICE_JSON_HOST = 'office-server.test.sips-atos.com'

SIPS_OFFICE_SECRET_KEY = 'CcDeXSiX2CY0mgbuB_MJxXqXYyJaINZixX2KZgY770o'
SIPS_OFFICE_JSON_MERCHANTID = '037107704346091'
SIPS_OFFICE_JSON_KEYVERSION	= '2'
SIPS_OFFICE_JSON_TEST_CARD_1 = '5017670000000000'
SIPS_EXPIRY_DATE = '201609'
SIPS_OFFICE_INTERFACE_VERSION = 'IR_WS_2.11'




# Response status codes
SUCCESS, MERCHANT_INVALID, TRANSACTION_INVALID, REQUEST_INVALID, SECURITY_ERROR, DUPLICATE_TRANSACTOIN = '00', '03', '12', '30', '34', '94'


def post(url, params):
	'''
	Deze methode voert het post request naar de sips paypage uit, en retourneert het antwoord van de server
	'''

	payload = urlencode(params)

	reponse = requests.post(url, payload, headers={'content-type': 'text/namevalue, charset=utf-8'})




class SipsRequest(object):
	'''
	Voorstelling van een SIPS request
	Een SIPS request is een POST naar 

	TESTING details:
	POST URL: 				https://payment-webinit.simu.sips-atos.com/rs-services/v2/paymentInit/
	SECRET KEY: 			002001000000001_KEY1

	merchantId:				002001000000001
	keyVersion:				1

	+ aanbeveling: stel transactionReference in
	transactionReference:	suikerboon_<some_ref> 

	'''

	def __init__(self, sips_url, merchantId='002001000000001', keyVersion='1', orderChannel='INTERNET', interfaceVersion='???', paymentMeanBrand='BCMC', paymentMeanType='CARD'):
		
		self._sips_url = sips_url
		self._merchantId = merchantId
		self._keyVersion = keyVersion
		self._orderChannel = orderChannel
		self._interfaceVersion = interfaceVersion
		self._paymentMeanBrand = paymentMeanBrand
		self._paymentMeanType = paymentMeanType



class SipsResponse(object):
	'''
	Voorstelling van een SIPS response
	Een SIPS response is een POST aan de automaticResponseUrl of manualResponseUrl (afhankelijk van de situatie)
	Er zijn 4 velden beschikbaar in het response:
	- Data (concatentation of response fields)
	- Ecode (gebruikte encoding)
	- Seal (Message signature)
	- interfaceVersion 
	'''

	def __init__(self, json_request, json_response):

		self.json_request = json_request
		self.json_response = json_response
		self.data = self._extract_data(json_response)

	def _extract_data(self, json_response):

		pass



class Gateway(object):

	def __init__(self, sips_url, merchantId='002001000000001', keyVersion='1', orderChannel='INTERNET', interfaceVersion='IR_WS_2.10', paymentMeanBrand='BCMC', paymentMeanType='CARD'):
		
		self._sips_url = sips_url
		self._merchantId = merchantId
		self._keyVersion = keyVersion
		self._orderChannel = orderChannel
		self._interfaceVersion = interfaceVersion
		self._paymentMeanBrand = paymentMeanBrand
		self._paymentMeanType = paymentMeanType


	def _initization_request(self, json_request):
		'''
		Deze methode voert het initialization request uit naar de SIPS connector URL, en ontvangt een response object 
		'''

		connection = httplib.HTTPSConnection(SIPS_PAYPAGE_TEST_HOST)
		headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
		connection.request('POST', SIPS_PAYPAGE_PATH)

	def _fetch_response(self, json_request):
		'''
		execute request
		'''

		base_url = 'http://127.0.0.1:8000'
		url_path = reverse('sips-place-order')

		#return_url = 'http://127.0.0.1:8000/checkout/thank-you/'
		#return_url = 'http://127.0.0.1:8000/checkout/sips/place-order/' # DEZE WERKTE!!!
		return_url = 'http://127.0.0.1:8000/checkout/preview/'


		amount = '1000'
		automaticResponseUrl = return_url
		currencyCode = '978'
		interfaceVersion = 'IR_WS_2.8'
		keyVersion = '1'
		merchantId = SIPS_PAYPAGE_MERCHANT	# TEST PAGE
		#merchantId = '225005017980001'		# LIVE PAGE
		#normalReturnUrl = return_url
		normalReturnUrl = return_url
		orderChannel = 'INTERNET'
		transactionReference = 'toptim104'
		#paymentMeanBrandList = ['VISA', 'MASTERCARD']

		request_dict = {
			'amount': amount,
			'automaticResponseUrl': automaticResponseUrl,
			'currencyCode' : currencyCode,
			'interfaceVersion': interfaceVersion,
			'keyVersion' : keyVersion,
			'merchantId': merchantId,
			'normalReturnUrl': normalReturnUrl,
			'orderChannel': orderChannel,
			'transactionReference': transactionReference,
		}

		concat_string = ''

		for key in sorted(request_dict):

			if key == 'keyVersion':
				continue

			elif key == 'sealAlgorithm':
				continue

			else: 
				concat_string += str(request_dict[key])


		SIPS_PAYPAGE_SECRET_KEY = '8TZkvnUF7pS6LjMNRNp5qzCVk2UKP8R6NHFmyuFPIhk'		# LIVE HOST
		SIPS_PAYPAGE_SECRET_KEY = '002001000000001_KEY1'							# TEST HOST

		# Bereken de secret key voor de huidige gegevens
		signature = self._calculate_seal(concat_string, SIPS_PAYPAGE_SECRET_KEY)

		request_dict['seal'] = signature


		try:
			response = requests.post(SIPS_PAYPAGE_URL, json=request_dict)				# TEST PAGE
			#response = requests.post(SIPS_PAYPAGE_URL_PRODUCTION, json=request_dict)	# LIVE PAGE

		except requests.ConnectionError:
			print 'godver'


		json_response = response.json()


		if json_response['redirectionStatusCode'] == '00':

			print '--------SIPS CONNECTOR: SUCCESS'

			url = str(json_response['redirectionUrl'])
			redirectionVersion = str(json_response['redirectionVersion'])
			redirectionData = str(json_response['redirectionData'])


			return url, redirectionVersion, redirectionData


		else:
			print '--------SIPS CONNECTOR: FAILURE'

			print 'error: ' + str(json_response['redirectionStatusCode'])
			print 'volledige error response: ' + str(json_response)

			if str(json_response['redirectionStatusCode']) == '94':

				raise UnableToTakePayment(mark_safe('Er werd reeds een transactie uitgevoerd met deze referentie. ' + \
					'Een duplicaat transactie wordt omwille van veiligheidsredenen niet toegelaten!'))

			#return 'http://127.0.0.1:8000/checkout/preview/', None, None, json_response['redirectionStatusCode']


		#return response.json()



	def _calculate_seal(self, concat_string, secret_key):
		'''
		Deze methode berekent de seal, alle vereiste velden worden als **kwargs parameters aangeboden
		De return value is een string die als seal geldt
		SHA encryptie seal: http://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python
		'''

		print '************** gateway: _calculate_seal()'

		message = bytes(concat_string).encode('utf-8')
		secret = bytes(secret_key) #.encode('utf-8')

		#secret = secret_key

		#message = bytes('Message').encode('utf-8')
		#secret = bytes('secret').encode('utf-8')

		#sig = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
		#sig = base64.b64encode(hmac.new('secret', 'Message', digestmod=hashlib.sha256).digest())

		#sig = hmac.new(secret, message, digestmod=hashlib.sha256).digest()

		sig = HMAC.new(key=secret, msg=message, digestmod=SHA256).hexdigest()

		print 'seal sig: ' + sig

		return sig


	def _check_kwargs(self, kwargs, required_keys):

		for key in required_keys:

			if not key in kwargs:
				raise ValueError('Je moet %s nog toevoegen als fieds')

		for key in kwargs:

			value = kwargs[key] # de waarde voor een bepaalde key

			if key == 'amount' and value == 0:
				raise ValueError('Een betaling kan niet 0 zijn')


	def pre(self, **kwargs):
		'''
		De pre methode wordt gebruikt om betaling onmiddellijk te innen vooraleer order processing plaats vindt. 
		Het is deze methode die door de Facade wordt opgeroepen
		'''

		return self._fetch_response(None)
