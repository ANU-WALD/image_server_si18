from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

wgs84_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'

albers_wkt = 'PROJCS["GDA94 / Australian Albers",GEOGCS["GDA94",DATUM["Geocentric_Datum_of_Australia_1994",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6283"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4283"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["standard_parallel_1",-18],PARAMETER["standard_parallel_2",-36],PARAMETER["latitude_of_center",0],PARAMETER["longitude_of_center",132],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","3577"]]'

min_lon = 122.0
max_lon = 123.0
min_lat = -18.0
max_lat = -17.0
im_size = 800

res = 1. / im_size

# You need to bring a LS8 numpy array for this region using the DEA
# We define an array here for this example
ls8_image = np.tile(np.arange(4000, dtype=np.int16),(4000,1))


src = gdal.GetDriverByName('MEM').Create('', 4000, 4000, 1, gdal.GDT_Int16)
src.GetRasterBand(1).WriteArray(ls8_image)

#These coordinates should come from the x and y axis of the DEA cube
src.SetGeoTransform([-1057968.7, 25.0, 0.0, -1853422.93, 0.0, -25.0])
src.SetProjection(albers_wkt)


#Now we set up another empty lat-lon raster to reproject into it
dst = gdal.GetDriverByName('MEM').Create('', im_size, im_size, 1, gdal.GDT_Float32)
dst.SetGeoTransform([min_lon, res, 0., max_lat, 0., -1*res])
dst.SetProjection(wgs84_wkt)

gdal.ReprojectImage(src, dst, None, None, gdal.GRA_NearestNeighbour)

plt.imsave("LS8.png", dst.ReadAsArray())
