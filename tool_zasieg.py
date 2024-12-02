import arcpy
import os
from klasy import Wierzcholek, Krawedz, Graf
from func import retrieve_path, create_reachability_map, add_shp_to_map, create_shp_from_path, create_reachability_shp
arcpy.env.overwriteOutput = True

'''
Parametry do toola:
0. fc FeatureLayer - warstwa z siecią dróg
1. warstwa_punktowa_zasieg FeatureLayer - warstwa punktowa z jednym obiektem
2. travel_time Double - czas w minutach
'''

graf = Graf()

fc = arcpy.GetParameterAsText(0)
warstwa_punktowa_zasieg = arcpy.GetParameterAsText(1)
travel_time = int(arcpy.GetParameterAsText(2)) * 60 # [s]
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

with arcpy.da.SearchCursor(warstwa_punktowa_zasieg, ['SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        x, y = row[0], row[1]
        points_zasieg.append((x,y))
        arcpy.AddMessage(points_zasieg)

if len(points_zasieg) == 1:
    x, y = points_zasieg[0]

    point_zasieg = graf.snap(x, y)
    arcpy.AddMessage(f"Point: {point_zasieg}")
    
else:
    arcpy.AddMessage("W warstwie punktowej do wyznaczenia zasięgu powinien znajdować się 1 punkt !")


spatial_reference = arcpy.Describe(fc).spatialReference
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
output_folder= "shp"
output_name_zasieg = "zasieg.shp"
output_path_zasieg = os.path.join(script_dir,output_folder, output_name_zasieg)

arcpy.management.CreateFeatureclass(output_folder, output_name_zasieg, "POLYLINE", spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name_zasieg}", "TravelTime", "FLOAT")
reachable_nodes, came_from=create_reachability_map(graf, point_zasieg.id, travel_time)
create_reachability_shp(graf,output_path_zasieg,reachable_nodes,came_from)
add_shp_to_map(output_path_zasieg)


output_folder= "shp"
output_name_zasieg = "zasieg_punkty.shp"
output_path_zasieg = os.path.join(script_dir,output_folder, output_name_zasieg)

arcpy.management.CreateFeatureclass(output_folder, output_name_zasieg, "POINT",spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name_zasieg}", "TIME", "FLOAT")

print("Węzły, do których można dotrzeć w maksymalnym czasie:")

with arcpy.da.InsertCursor(f"{output_folder}/{output_name_zasieg}", ["TIME", "SHAPE@"]) as cursor:
    for node in reachable_nodes:
        print(node)
        cursor.insertRow([reachable_nodes[node], arcpy.PointGeometry(arcpy.Point(node.split(",")[0], node.split(",")[1]), spatial_reference)])
