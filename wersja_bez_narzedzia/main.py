import arcpy
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from klasy import Wierzcholek, Krawedz, Graf
from func import a_star, retrieve_path, create_reachability_map, create_shp_from_path

arcpy.env.overwriteOutput = True
graf = Graf()

fc = "skjz\direction_calosc_0.shp"

start_point = graf.snap(474638, 572636)
end_point = graf.snap(471582, 576616)

warstwa_punktowa_zasieg = 'test_data\punkt_do_zasiegu.shp'
travel_time = 1*60 
points_zasieg = []

with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@', 'klasaDrogi', 'kierunek']) as cursor:
    for row in cursor:
        startPoint = row[1].firstPoint
        endPoint = row[1].lastPoint
        geometry = row[1].WKT

        x1 = startPoint.X
        y1 = startPoint.Y

        x2 = endPoint.X
        y2 = endPoint.Y

        edge_id = row[0]
        length = int(row[1].length)
        road_class = row[2]
        direction = row[3]

        start_id = str(int(x1)) + "," + str(int(y1))
        end_id = str(int(x2)) + "," + str(int(y2))
        
        start_node = graf.add_node(start_id, x1, y1)
        end_node = graf.add_node(end_id, x2, y2)

        start = Wierzcholek(start_id, x1, y1)
        end = Wierzcholek(end_id, x2, y2)
        edge = Krawedz(edge_id, start_node, end_node, length, road_class, direction, geometry)
        graf.add_edge(edge)
    
with open('nodes.txt', 'w') as f:
    for node in graf.nodes.values():
        f.write(f"{node.id}\n")
   
came_from_distance, cost_so_far_distance = a_star(graf, start_point, end_point, 'distance')
length_a_star_distance = cost_so_far_distance[end_point.id]
path_distance = retrieve_path(came_from_distance, start_point.id, end_point.id)

came_from_time, cost_so_far_time = a_star(graf, start_point, end_point, 'time')
length_a_star_time = cost_so_far_time[end_point.id]
path_time = retrieve_path(came_from_time, start_point.id, end_point.id)

#----------wizualizacja----------------
spatial_reference = arcpy.Describe(fc).spatialReference
output_folder= "shp"
output_name_distance = "path_distance.shp"
output_name_time = "path_time.shp"

arcpy.management.CreateFeatureclass(output_folder, output_name_distance, "POLYLINE", spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name_distance}", "NR", "FLOAT")
arcpy.management.CreateFeatureclass(output_folder, output_name_time, "POLYLINE", spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name_time}", "NR", "FLOAT")    
create_shp_from_path(graf,path_distance, output_folder, output_name_distance, spatial_reference)
create_shp_from_path(graf,path_time, output_folder, output_name_time, spatial_reference)

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
output_path_distance = os.path.join(script_dir,output_folder, output_name_distance)
output_path_time = os.path.join(script_dir,output_folder, output_name_time)

with arcpy.da.SearchCursor(warstwa_punktowa_zasieg, ['SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        x, y = row[0], row[1]
        points_zasieg.append((x,y))

if len(points_zasieg) == 1:
    x, y = points_zasieg[0]
    point_zasieg = graf.snap(x, y)
else:
    print("W warstwie punktowej do wyznaczenia zasięgu powinien znajdować się 1 punkt !")
    exit()

output_name_zasieg = "zasieg.shp"
arcpy.management.CreateFeatureclass(output_folder, output_name_zasieg, "POLYLINE", spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name_zasieg}", "NR", "FLOAT")
reachable_nodes, came_from=create_reachability_map(graf, point_zasieg.id, travel_time)
for node_id in reachable_nodes:
    path = retrieve_path(came_from, point_zasieg.id, node_id)
    create_shp_from_path(graf,path, output_folder, output_name_zasieg, spatial_reference)
    
output_path_zasieg = os.path.join(script_dir,output_folder, output_name_zasieg)