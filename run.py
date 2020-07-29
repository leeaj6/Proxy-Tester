'''
Author: Alexander Lee

Run file for proxy tester

python run.py SITE_DOMAIN TIMEOUT
(i.e. python run.py www.google.com 10)
'''

from ProxyTester import *
import sys

# Attempt to read in proxies from proxies.txt
try:
  proxy_list_main = [(line.rstrip('\n').split(":")[2]+":"+line.rstrip('\n').split(":")[3]+"@"+line.rstrip('\n').split(":")[0]+":"+line.rstrip('\n').split(":")[1]) for line in open('proxies.txt')]
except:
  try:
    proxy_list_main = [line.rstrip('\n') for line in open('proxies.txt')]
  except:
    proxy_list_main = []

# Test if proxies are available
if len(proxy_list_main):
	proxy_list_main = ProxyTester(proxy_list_main, sys.argv[1], sys.argv[2]).testAll()
	open("good-proxies.out", "w").write('\n'.join(proxy_list_main))
else:
	print("No proxies found")