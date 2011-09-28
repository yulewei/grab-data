import pyproj;
from pyproj import Proj;

p900913 = "+title= Google Mercator EPSG:900913 +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs";
p2431 = "+proj=tmerc +lat_0=30.1533 +lon_0=120.0612 +k=1 +x_0=70000 +y_0=70000 +ellps=krass +units=m +no_defs";
p4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

p1 = Proj(p2431)
p2 = Proj(p4326)

x1, y1 = 88272.1719, 88360.2656
x2, y2 = pyproj.transform(p1, p2, x1, y1)
print (x1, y1);
print (x2, y2);
