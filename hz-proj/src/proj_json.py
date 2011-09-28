import math
import pyproj;
from pyproj import Proj;

import json


p900913 = "+title= Google Mercator EPSG:900913 +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs";
p2431 = "+proj=tmerc +lat_0=30.1533 +lon_0=120.0612 +k=1 +x_0=70000 +y_0=70000 +ellps=krass +units=m +no_defs";
p4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

p1 = Proj(p2431)
p2 = Proj(p4326)


for i in range(0, 53):
    if i == 34 or i == 45:
        continue

    fin = open("json/{0}.txt".format(i), "r", -1, 'utf-8')

    data = fin.read()
    obj = json.loads(data)

    print(i, type(obj))

    geotype = obj["geometryType"]
    features = obj["features"]

#    print(geotype)
#    print(type(features))

    for item in features:
        geo = item["geometry"]

        if geotype == "esriGeometryPoint":
            # 注意图层4, "OBJECTID" : 444, x,y值为NaN, 加上特殊判断
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

#    str = json.dumps(obj).encode();
    str = json.dumps(obj, ensure_ascii = False).encode();
    fout = open("proj/{0}.txt".format(i), "wb")
    fout.write(str);
    fout.close()

