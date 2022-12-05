#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import fiona
import geopandas as gpd
import glob
from shapely.geometry import Point, LineString, Polygon
from rasterstats import zonal_stats


# In[2]:


data1 = pd.read_csv('./Lab2Data/districts/district01.txt', sep='\t')
data5 = pd.read_csv('./Lab2Data/districts/district05.txt', sep='\t')
data6 = pd.read_csv('./Lab2Data/districts/district06.txt', sep='\t')


# In[3]:


data01 = data1.values
data1_polygon = Polygon(data01)

data05 = data5.values
data2_polygon = Polygon(data05)

data06 = data6.values
data3_polygon = Polygon(data06)


# In[4]:


data1_polygon


# In[5]:


data2_polygon


# In[6]:


data3_polygon


# In[7]:


districts = {}
num_coords01gdf = ("Vertices"),(data01.shape[0])
num_coords05gdf = ("Vertices"),(data05.shape[0])
num_coords06gdf = ("Vertices"),(data06.shape[0])

numbers = ['1', '2', '3']

district = ['01', '05', '06'] 

num_coords = [num_coords01gdf, 
     num_coords05gdf,
               num_coords06gdf]

for idx, dist in enumerate(numbers):
    districts[dist] = {'district': district[idx],'num_coords': num_coords[idx]}
    
print(districts)


# In[8]:


districts_df = pd.DataFrame(districts)
districts_df_2 = pd.DataFrame.from_dict(districts, orient='index')
districts_gdf = gpd.GeoDataFrame(districts_df_2)
districts_gdf


# In[9]:


ag04 = './Lab2Data/agriculture/GLOBCOVER_2004_lab2.tif' 
ag09 = './Lab2Data/agriculture/GLOBCOVER_2009_lab2.tif' 

geodata1 = gpd.GeoDataFrame(data=[{'districtID': 'distrcit_1'}], geometry=[data1_polygon])
geodata1.to_file(filename='dPolygon1.shp', driver='ESRI Shapefile')
geodf1 = gpd.read_file('dPolygon1.shp')

geodata2 = gpd.GeoDataFrame(data=[{'districtID': 'distrcit_2'}], geometry=[data2_polygon])
geodata2.to_file(filename='dPolygon2.shp', driver='ESRI Shapefile')
geodf2 = gpd.read_file('dPolygon2.shp')

geodata3 = gpd.GeoDataFrame(data=[{'districtID': 'distrcit_3'}], geometry=[data3_polygon])
geodata3.to_file(filename='dPolygon3.shp', driver='ESRI Shapefile')
geodf3 = gpd.read_file('dPolygon3.shp')


# In[10]:


zdata1_04 = zonal_stats(geodf1,ag04,stats=['count','sum'])
zdata1_04


# In[11]:


zdata2_04 = zonal_stats(geodf2, ag04, stats=['count','sum'])
zdata2_04


# In[12]:


zdata3_04 = zonal_stats(geodf3, ag04, stats=['count','sum'])
zdata3_04


# In[13]:


zdata1_09 = zonal_stats(geodf1, ag09, stats=['count','sum'])
zdata1_09


# In[14]:


zdata2_09 = zonal_stats(geodf2, ag09, stats=['count','sum'])
zdata2_09


# In[15]:


zdata3_09 = zonal_stats(geodf3, ag09, stats=['count','sum'])
zdata3_09


# In[16]:


df104 = pd.DataFrame(zdata1_04)
ag104 = round((df104['sum']/df104['count']) * 100)
ag104


# In[17]:


df204 = pd.DataFrame(zdata2_04)
ag204 = round((df204['sum']/df204['count']) * 100)
ag204


# In[18]:


df304 = pd.DataFrame(zdata3_04)
ag304 = round((df304['sum']/df304['count']) * 100)
ag304


# In[19]:


df109 = pd.DataFrame(zdata1_09)
ag109 = round((df109['sum']/df109['count']) * 100)
ag109


# In[20]:


df209 = pd.DataFrame(zdata2_09)
ag209 = round((df209['sum']/df209['count']) * 100)
ag209


# In[21]:


df309 = pd.DataFrame(zdata3_09)
ag309 = round((df309['sum']/df309['count']) * 100) 
ag309


# In[22]:


frames = [df104, df204, df304, df109, df209, df309]

result = pd.concat(frames)
result


# In[23]:


agdistricts = {}

numbers = ['dist1_04', 'dist2_04', 'dist3_04', 'dist1_09', 'dist2_09', 'dist3_09'] 

agricultural_pixel_percent = [ag104, 
              ag204, 
              ag304, 
              ag109, 
              ag209,
              ag309]


for idx, dist in enumerate(numbers):
    agdistricts[dist] = {'agricultural_pixel_percent': agricultural_pixel_percent[idx]}

ag_df = pd.DataFrame.from_dict(agdistricts, orient='index')
ag_df #shows the district, year and the % of agriculture pixels


# In[26]:


lst = [] #trail and fail...

for districts, rows in result.iterrows():
    pixper = round(rows['sum']/rows['count'] * 100)
    x = 0
    districts= x+1
    #districts = numbers
    print(f'districts: {x}', 'pixper: {pixper}')

