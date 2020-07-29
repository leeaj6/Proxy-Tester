'''
Author: Alexander Lee

ProxyTester.py

Custom Proxy Tester
'''

import requests
import time
import threading

class ProxyTester(object):
	"""Custom Proxy Tester Solution"""
	def __init__(self, proxy_list:list, site_domain:str, timeout:int):
		self.proxy_list = proxy_list
		self.site_domain = site_domain.replace('https://', '').replace('http://', '')
		self.timeout = timeout

	def testProxy(self, proxy:str) -> None:
		status = None
		try:
			start = time.time()
			response = requests.get('https://'+self.site_domain, proxies={'http': 'http://' + proxy, 'https': 'https://' + proxy}, timeout=self.timeout)
			end = time.time()
		except:
			status = {
				'proxy': proxy, 
				'valid': False,
				'status_code': None,
				'speed': None
			}
		else:
			status = {
				'proxy': proxy,
				'valid': True,
				'status_code': response.status_code,
				'speed': round((end - start)*1000)
			}
				
		if status != None and status['valid']:
			# The proxy may be valid (connects properly); however, it is useless if the IP is banned
			if status['status_code'] in (403, 429, 420):
				self.banned_proxies.append(status)
			else:
				self.valid_proxies.append(status)
		else:
			self.bad_proxies.append(status)

	def testAll(self) -> list:
		result = []

		self.valid_proxies = []
		self.banned_proxies = []
		self.bad_proxies = []

		for proxy in self.proxy_list:
			threading.Thread(target=self.testProxy, args=(proxy,)).start()

		# Check condition that all proxies have been tested before returning results
		while(len(self.valid_proxies)+len(self.banned_proxies)+len(self.bad_proxies) != len(self.proxy_list)):
			time.sleep(5)

		print()
		print('RESULTS FOR '+self.site_domain)
		print(self._printGreen('[{}] - {} ({})'.format(time.asctime(time.localtime(time.time())), 'GOOD PROXIES', len(self.valid_proxies))))
		print(self._printYellow('[{}] - {} ({})'.format(time.asctime(time.localtime(time.time())), 'BANNED PROXIES', len(self.banned_proxies))))
		print(self._printRed('[{}] - {} ({})'.format(time.asctime(time.localtime(time.time())), 'BAD PROXIES', len(self.bad_proxies))))
		print()
		print('_'*89)
		print('|{}|{}|{}|'.format('PROXY ADDRESS'.center(50, ' '), 'STATUS'.center(25, ' '), 'SPEED'.center(10, ' ')))
		print('_'*89)
		for good_proxy in self.valid_proxies:
			print(self._printGreen('|{}|{}|{}|'.format((good_proxy['proxy']).center(50, ' '), ("GOOD "+str(good_proxy['status_code'])).center(25, ' '), (str(good_proxy['speed'])+' ms').center(10, ' '))))
			result.append(good_proxy['proxy'])
		for banned_proxy in self.banned_proxies:
			print(self._printYellow('|{}|{}|{}|'.format((banned_proxy['proxy']).center(50, ' '), ("BANNED "+str(banned_proxy['status_code'])).center(25, ' '), (str(banned_proxy['speed'])+' ms').center(10, ' '))))
		for bad_proxy in self.bad_proxies:
			print(self._printRed('|{}|{}|{}|'.format((bad_proxy['proxy']).center(50, ' '), ("BAD "+str(bad_proxy['status_code'])).center(25, ' '), str(bad_proxy['speed']).center(10, ' '))))
		print('_'*89)

		return result

	# Colorize prints
	def _printRed(self, statement:str) -> str: 
		return ("\033[91m{}\033[00m".format(statement))

	def _printGreen(self, statement:str) -> str: 
		return ("\033[92m{}\033[00m".format(statement))

	def _printYellow(self, statement:str) -> str:
		return ("\033[93m{}\033[00m".format(statement))
