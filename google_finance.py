import urllib
import re

GOOGLE_FINANCE_BASE_URL = 'http://www.google.com/finance'
# GOOGLE_FINANCE_BASE_URL = 'http://106.187.39.173/gf/'

REALTIME_INFO_KV_PATTERN = re.compile('^,?"(.*)"\s*:\s*"(.*)"')
REALTIME_INFO_FLOAT_KEYS = ('l', 'l_cur', 'l_fix', 'c', 'cp_fix', 'c_fix', 's', 'pcls_fix', 'cp')

def getQuotes(s):
	url = GOOGLE_FINANCE_BASE_URL+'?q=%s' % s
	print url
	data = readUrl(url)
	return data

def getRealtimeInfo(s):
	url = GOOGLE_FINANCE_BASE_URL+'/info?q=%s' % s
	data = readUrl(url)
	info = {}
	for line in data.split('\n'):
		m = REALTIME_INFO_KV_PATTERN.match(line)
		if m:
			k, v = m.groups()
			info[k] = v

	info['id'] = int(info['id'])

	for k in REALTIME_INFO_FLOAT_KEYS:
		try:
			info[k] = float(info[k])
		except:
			pass

	return info

def readUrl(url):
	fd = urllib.urlopen(url)
	data = fd.read()
	fd.close()
	return data

if __name__ == '__main__':
	print getRealtimeInfo('SPY')
	print getQuotes('SPY')

