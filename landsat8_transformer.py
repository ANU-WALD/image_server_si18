from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

wgs84_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

min_lon = 120.0
max_lon = 124.0
min_lat = -20.0
max_lat = -16.0
im_size = 800

res = 4. / im_size

# You need to create a LS8 file for this region using the DEA
src_path = ""

src = gdal.Open(src_path)
print(src.GetGeoTransform())
print(src.GetProjection())

dst = gdal.GetDriverByName('MEM').Create('', im_size, im_size, 1, gdal.GDT_Float32)
geot = [min_lon, res, 0., max_lat, 0., -1*res]
dst.SetGeoTransform(geot)
dst.SetProjection(wgs84_wkt)

gdal.ReprojectImage(src, dst, None, None, gdal.GRA_NearestNeighbour)

plt.imsave("LS8.png", dst.ReadAsArray())
