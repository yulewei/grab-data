import urllib.request
import urllib.parse

#params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#f = urllib.request.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
#print(f.read().decode('utf-8'))


url_tmp = "http://220.191.211.111/ArcGIS/rest/services/ghj_map/MapServer/{0}/query?{1}"
url_tmp = "http://220.191.211.111/ArcGIS/rest/services/unit/MapServer/{0}/query?{1}"

query_str = {'f' : 'json', 'returnGeometry' : 'true', 'where' : 'true', 'outFields' : '*' };
query_str = {'f' : 'json', 'returnGeometry' : 'true', 'where' : 'OBJECTID > 0', 'outFields' : 'OBJECTID' };

query_str = urllib.parse.urlencode (query_str);

for i in range(0, 1):
    if i == 34 or i == 45:
        continue

    url = url_tmp.format(i, query_str)
    fin = urllib.request.urlopen (url)
    data = fin.read();

    fout = open("json/ghj_map/{0}.txt".format(i), "wb")
    fout.write(data);
    fout.close()
