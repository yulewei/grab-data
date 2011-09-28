import urllib.request
import json
import os
import math
import pyproj;
from pyproj import Proj;

def prj_featrue(p1, p2, obj):
    geotype = obj["geometryType"]
    features = obj["features"]

    for item in features:
        geo = item["geometry"]

        if geotype == "esriGeometryPoint":
            # 注意ghj_map图层4, "OBJECTID" : 444, x,y值为NaN, 加上特殊判断
            if math.isnan(geo["x"]) or math.isnan(geo["y"]):
                continue
            geo["x"], geo["y"] = pyproj.transform(p1, p2, geo["x"], geo["y"])
        elif geotype == "esriGeometryPolyline":
            paths = geo["paths"]
            for path in paths:
                for pt in path:
                    pt[0], pt[1] = pyproj.transform(p1, p2, pt[0], pt[1])
        elif geotype == "esriGeometryPolygon":
            rings = geo["rings"]
            for ring in rings:
                for pt in ring:
                    pt[0], pt[1] = pyproj.transform(p1, p2, pt[0], pt[1])


p900913 = "+title= Google Mercator EPSG:900913 +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs";
p2431 = "+proj=tmerc +lat_0=30.1533 +lon_0=120.0612 +k=1 +x_0=70000 +y_0=70000 +ellps=krass +units=m +no_defs";
p4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

p1 = Proj(p2431)
p2 = Proj(p4326)


root_url = "http://220.191.211.111/ArcGIS/rest/services/?f=json"

fin = urllib.request.urlopen (root_url)
data = fin.read().decode()
services = json.loads(data)["services"]

serlist = []
for server in services:
    if server["type"] == "MapServer":
        serlist.append(server["name"])

#print(serlist)

serlist = ["ghj_map", "unit"]
#serlist = ["unit"]

ser_url = "http://220.191.211.111/ArcGIS/rest/services/{}/MapServer/?f=json"
layer_url = "http://220.191.211.111/ArcGIS/rest/services/{}/MapServer/{}?f=json"
query_url = "http://220.191.211.111/ArcGIS/rest/services/{}/MapServer/{}/query?{}"
query_str = {'f' : 'json', 'returnGeometry' : 'true', 'where' : 'OBJECTID > 0', 'outFields' : 'OBJECTID' };
query_str = urllib.parse.urlencode (query_str);

for server in serlist:
    fin = urllib.request.urlopen (ser_url.format(server))
    data = fin.read().decode()
    layers = json.loads(data)["layers"]
    for layer in layers:
        fin = urllib.request.urlopen (layer_url.format(server, layer["id"]))
        data = fin.read().decode()
        layer_info = json.loads(data)
        if layer_info["type"] != "Feature Layer":
            continue
        fin = urllib.request.urlopen (query_url.format(server, layer["id"], query_str))
        data = fin.read().decode()
        obj = json.loads(data)
        prj_featrue(p1, p2, obj)
        data = json.dumps(obj, ensure_ascii = False).encode();

        if not os.path.exists("proj/" + server):
            os.mkdir("proj/" + server)
        fout = open("proj/{}/{}.json".format(server, layer_info["id"]), "wb")
        fout.write(data);
        fout.close()

        print(server, layer_info["id"], layer_info["name"], "saved")

