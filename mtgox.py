import urllib
import urllib2
import json
import time
import hashlib
import hmac
import base64


def sign_data(secret, data):
    return base64.b64encode(str(hmac.HMAC(secret, data, hashlib.sha512).digest()))

 
class MtGox():

	def __init__(self, auth_key, auth_secret, currency):
		self.auth_key = auth_key
		self.auth_secret = base64.b64decode(auth_secret)
		self.currency = currency

	def request(self, path):
		data = urllib.urlencode({"nonce": int(time.time()*100000),})
		hash_data = path + chr(0) + data
		header = {
			'User-Agent': 'Gekkox',
			'Rest-Key': self.auth_key,
			'Rest-Sign': sign_data(self.auth_secret, hash_data),
		}
		req = urllib2.Request('https://data.mtgox.com/api/2/' + path, data, header)
		try:
			res = urllib2.urlopen(req)
			return json.load(res)
		except urllib2.HTTPError, error:
		    print error.read()	
		except Exception as e:
			print str(e)
		return {'result': 'failed'}

	def ticker_data(self):
		"""Get ticker data"""
		path = "BTC" + self.currency + "/money/ticker"
		return self.request(path)
		
	def lag(self):
		"""Get ticker data"""
		path = "BTC" + self.currency + "/money/order/lag"
		return self.request(path)
		
	def get_info(self):
		"""Get your current balance."""
		path = "BTC" + self.currency + "/money/info"
		return self.request(path)
























class test():

	def market_depth(self):
		"""Get market depth"""
		api = "data/getDepth.php"
		return self._curl_mtgox(api=api)

	def recent_trades(self):
		"""Get recent trades

		   Returns
		   -------
		   A list of dicts:
				 {u'amount': 60,
				  u'date': 1306775375,
				  u'price': 8.7401099999999996,
				  u'tid': u'93842'},

		"""

		api = "data/getTrades.php"
		return self._curl_mtgox(api=api)

	@property
	def snapshot(self):
		"""Get current BBO
		"""
		order_book = self.market_depth()
		return dict(
			bid=order_book['bids'][0][0],
			ask=order_book['asks'][0][0],
			size_bid=order_book['bids'][0][1],
			size_ask=order_book['asks'][0][1],
			)

# Authentication required methods
	def authenticate(self, username, password):
		"""Set MtGox authentication information"""
		self.username = username
		self.password = password

	def authentication_required(function):
		def wrapped(self, *args, **kwargs):
			if not (self.username and self.password):
				msg = "You must be authenticated to use this method"
				raise Exception, msg
			else:
				return function(self, *args, **kwargs)
		return wrapped

	@authentication_required
	def funds(self):
		"""Get your current balance."""
		api = "getFunds.php"
		postdict = {
			'name':self.username,
			'pass':self.password,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	@authentication_required
	def buy(self, amount, price):
		"""Place a buy order.

		   Returns list of your open orders

		"""

		api = "buyBTC.php"
		postdict = {
			'name':   self.username,
			'pass':   self.password,
			'amount': amount,
			'price':  price,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	@authentication_required
	def sell(self, amount, price):
		"""Place a sell order.

		   Returns list of your open orders

		"""

		api = "sellBTC.php"
		postdict = {
			'name':   self.username,
			'pass':   self.password,
			'amount': amount,
			'price':  price,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	@authentication_required
	def open_orders(self):
		"""Get open orders.

		   In response, these keys:
			   oid:	Order ID
			   type:   1 for sell order or 2 for buy order
			   status: 1 for active, 2 for not enough funds

		"""

		api = "getOrders.php"
		postdict = {
			'name':   self.username,
			'pass':   self.password,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	@authentication_required
	def cancel(self, oid, order_type):
		"""Cancel an existing order.

		   oid: Order ID
		   type: 1 for sell order or 2 for buy order

		"""

		api = "cancelOrder.php"
		postdict = {
			'name':   self.username,
			'pass':   self.password,
			'oid':	oid,
			'type':   order_type,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	@authentication_required
	def send(self, btca, amount, group1="BTC"):
		"""Send BTC to someone.

		   btca:	 bitcoin address to send to
		   amount:   amount

		   Not really sure what this does or what the 'group1' arg is for,
		   just copying from the API.

		   https://mtgox.com/code/withdraw.php?name=blah&pass=blah&group1=BTC&btca=bitcoin_address_to_send_to&amount=#

		"""

		# In [3]: m.send(btca="17kXoRWgeTRAyVhyJoMeZz5xHz98xPoiA", amount=1.98)
		# Out[3]: {u'error': u'Not available yet'}


		api = "withdraw.php"
		postdict = {
			'name':   self.username,
			'pass':   self.password,
			'btca':   btca,
			'amount': amount,
			}
		return self._curl_mtgox(api=api, postdict=postdict)

	def _curl_mtgox(self, api, postdict=None, timeout=8):
		print "hello"
		BASE_URL = "https://data.mtgox.com/api/2/"
		url = BASE_URL + api
		print url
		if postdict:
			postdata = urllib.urlencode(postdict)
			request = urllib2.Request(url, postdata)
		else:
			request = urllib2.Request(url)
		response = urllib2.urlopen(request, timeout=timeout)
		return json.loads(response.read())
