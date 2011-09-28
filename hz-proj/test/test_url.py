import urllib.request
import urllib.parse

params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
f = urllib.request.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
print(f.read().decode('utf-8'))
