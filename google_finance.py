import urllib
import re
import sys

# GOOGLE_FINANCE_BASE_URL = 'http://www.google.com/finance'
GOOGLE_FINANCE_BASE_URL = 'http://106.187.39.173/gf/'

REALTIME_INFO_KV_PATTERN = re.compile('^,?"(.*)"\s*:\s*"(.*)"')

QUOTES_KV_PATTERN = re.compile('<td class="key"\s*data-snapfield="(.*?)">.*?</td>\s*<td class="val">(.*?)</td>')

def getQuotes(s):
	url = GOOGLE_FINANCE_BASE_URL+'?q=%s' % s
	data = readUrl(url)
	data = data.replace('\n', ' ')
	# <td class="key"           data-snapfield="vol_and_avg">Vol. </td> <td class="val">13,009.00 </td>
	quotes = {}
	for k, v in QUOTES_KV_PATTERN.findall(data):
		v = v.replace('&nbsp;', '').strip()
		quotes[k] = v
	
	return quotes

	

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
	for k, v in info.items():
		if k == 'id': continue 
		try:
			v = float(v)
		except:
			pass

		info[k] = v

	return info

def readUrl(url):
	print >>sys.stderr, "RETRIVE %s" % url
	fd = urllib.urlopen(url)
	data = fd.read()
	fd.close()
	return data

if __name__ == '__main__':
	#for k, v in getRealtimeInfo('SPY').iteritems():
	#	print '\t', k, '=', v
	print getQuotes('SPY')

