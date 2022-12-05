#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import fiona
import pandas as pd

layers = fiona.listlayers('lab1.gpkg')
slist = []
mlist = []
map_id = []
for layer_types in layers:
    if layer_types.startswith('soilmu'):
        slist.append(gpd.read_file('lab1.gpkg', layer = layer_types))
        map_id.append(layer_types[-5:])
    elif layer_types.startswith('muaggatt'):
        mlist.append(gpd.read_file('lab1.gpkg', layer = layer_types))


# In[2]:


x = 0
merge_layers = []
for x in range(0,9):
        merged_layers = slist[x].merge(mlist[x],left_on='MUSYM', right_on='musym', how = 'left')
        merged_layers['mapunit'] = map_id[x]
        x = x+1
        merge_layers.append(merged_layers)
        merge_layers0 = gpd.GeoDataFrame(merged_layers)
        merge_layers0.set_geometry('geometry_x')
        watershed = gpd.read_file('lab1.gpkg', layer = 'wbdhu8_lab1')
        concatenated_layer = pd.concat([watershed, merge_layers0], axis="columns")
concatenated_layer.head(2)


# In[3]:


print('There seems to be two intersects with the watershed boundaries at St. Vrain and Big Thompson CO!')

