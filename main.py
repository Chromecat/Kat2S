import folium

maplayer = folium.Map(location=[50.920652, 6.937008],
                      tiles="Stamen Toner",
                      zoom_start=15
                      )

geolayer = folium.FeatureGroup()

geolayer.add_child(folium.GeoJson(open("test.geojson",
                                       encoding="utf-8-sig",
                                       ).read()))

geolayer.add_to(maplayer)

maplayer.save('test.html')
