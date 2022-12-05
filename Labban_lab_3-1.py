import sys
import pandas as pd
import fiona
import geopandas as gpd
import glob
from shapely.geometry import Point, LineString, Polygon
from rasterstats import zonal_stats
import numpy as np
import random
import matplotlib.pyplot as plt

File='.Documents/PythonGIS/lab3.gpkg'
NewFile = gpd.read_file('Documents/PythonGIS/lab3.gpkg')
File_bounds = NewFile.total_bounds
HUC_w = fiona.listlayers(File)
ssurgo=gpd.read_file(File, layer='ssurgo_mapunits_lab3')

np.random.seed(0)
HUC = []
for w in HUC_w:
    if "wdbhuc" in w:
        HUC.append(w)
        
sample_points8 = {'point_id': [], 'geometry':[], 'HUC8': []}

for p in HUC:
    HUC8_w_gdf = gpd.read_file('Documents/PythonGIS/lab3.gpkg', layer='wdbhuc8')
    for idx, row in HUC8_w_gdf.iterrows():
        huc8_bounds = row['geometry'].bounds
        hucsqkm = row["Shape_Area"]/1000000
        nearinthuc8=(int(round(hucsqkm*0.05)))
        s8 = 0
        while s8 < nearinthuc8:
            x8 = (random.uniform(huc8_bounds[0], huc8_bounds[2]))
            y8 = (random.uniform(huc8_bounds[1], huc8_bounds[3]))
            point8 = Point(x8,y8)
            
            if row['geometry'].contains(point8):
                sample_points8['geometry'].append(point8)
                sample_points8['point_id'].append(row['HUC8'][:8])
                sample_points8['HUC8'].append('HUC8')
                s8 += 1

np.random.seed(0)
HUC = []
for w in HUC_w:
    if "wdbhuc" in w:
        HUC.append(w)
        
sample_points12 = {'point_id': [], 'geometry':[], 'HUC12': []}

for p in HUC:
    HUC12_w_gdf = gpd.read_file('Documents/PythonGIS/lab3.gpkg', layer='wdbhuc12')
    for idx, row in HUC12_w_gdf.iterrows():
        huc12_bounds = row['geometry'].bounds
        hucsqkm = row["Shape_Area"]/1000000
        nearinthuc12=(int(round(hucsqkm*0.05)))
        s12 = 0
        while s12 < nearinthuc12:
            x12 = (random.uniform(huc12_bounds[0], huc12_bounds[2]))
            y12 = (random.uniform(huc12_bounds[1], huc12_bounds[3]))
            point12 = Point(x12,y12)
            
            if row['geometry'].contains(point12):
                sample_points12['geometry'].append(point12)
                sample_points12['point_id'].append(row['HUC12'][:8])
                sample_points12['HUC12'].append('HUC12')
                s12 += 1

sample_points8_gdf = gpd.GeoDataFrame(sample_points8)
sample_points12_gdf = gpd.GeoDataFrame(sample_points12)
sample_points8_gdf = sample_points8_gdf.set_crs("EPSG:26913")
sample_points12_gdf = sample_points12_gdf.set_crs("EPSG:26913")

new_huc8 = gpd.sjoin(sample_points8_gdf, ssurgo, how='right')
new_huc12 = gpd.sjoin(sample_points12_gdf, ssurgo, how='right')

print("HUC8")
f_HUC_8 = new_huc8.groupby(by=['point_id']).mean()
print(f_HUC_8['aws0150'])

print("HUC12")
f_HUC_12 = new_huc12.groupby(by=['point_id']).mean()
print(f_HUC_12['aws0150'])

print("I think that the means are different between HUC8 and HUC12 because HUC12 has more points displayed compared to HUC8 as well as HUC12 is stored within HUC8.")
