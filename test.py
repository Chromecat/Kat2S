import os
import folium
from folium import FeatureGroup, LayerControl, Map, Marker

m = Map(
    location=[45.372, -121.6972],
    zoom_start=12,
    tiles='Stamen Terrain'
)

feature_group = FeatureGroup(name='Some icons')
Marker(location=[45.3288, -121.6625],
       popup='Mt. Hood Meadows').add_to(feature_group)

Marker(location=[45.3311, -121.7113],
       popup='Timberline Lodge').add_to(feature_group)

feature_group.add_to(m)
LayerControl().add_to(m)

m.save(os.path.join('FeatureGroup.html'))

style = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF'}

folium.GeoJson(combined,
               tooltip=folium.GeoJsonTooltip(fields=['LGA','MBRS'],
                                             aliases=['Location','Members']),
               style_function=lambda x: style).add_to(m)