import arcpy
import os
from klasy import Wierzcholek, Krawedz, Graf
from func import a_star, retrieve_path, create_reachability_map,add_shp_to_map,create_shp_from_path

arcpy.env.overwriteOutput = True
warstwa_punktowa = arcpy.GetParameterAsText(0)
fc = arcpy.GetParameterAsText(1)
# fc = "skjz\direction_calosc_0.shp"
graf = Graf()

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
        
with arcpy.da.SearchCursor(warstwa_punktowa, ['SHAPE@X','SHAPE@Y']) as cursor:
    arcpy.AddMessage(cursor)
    points =[]
    for row in cursor:
        x, y = row[0], row[1]
        points.append((x,y))

if len(points) == 2:
    start_x, start_y = points[0]
    end_x, end_y = points[1]

    start_point = graf.snap(start_x, start_y)
    end_point = graf.snap(end_x, end_y)

    arcpy.AddMessage(f"Start Point: {start_point}")
    arcpy.AddMessage(f"End Point: {end_point}")
else:
    arcpy.AddMessage("W warstwie punktowej powinny znajdować się 2 punkty !")
    
with open('nodes.txt', 'w') as f:
    for node in graf.nodes.values():
        f.write(f"{node.id}\n")
   
# start_point = graf.snap(474638, 572636)
# end_point = graf.snap(471582, 576616)

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
create_shp_from_path(graf,path_distance, output_folder, output_name_distance, spatial_reference)
create_shp_from_path(graf,path_time, output_folder, output_name_time, spatial_reference)

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
output_path_distance = os.path.join(script_dir,output_folder, output_name_distance)
add_shp_to_map(output_path_distance)
output_path_time = os.path.join(script_dir,output_folder, output_name_time)
add_shp_to_map(output_path_time)


output_name = "points.shp"

arcpy.management.CreateFeatureclass(output_folder, output_name, "POINT",spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name}", "TIME", "FLOAT")

reachability_map = create_reachability_map(graf, start_point.id, 900)
print("Węzły, do których można dotrzeć w maksymalnym czasie:")

with arcpy.da.InsertCursor(f"{output_folder}/{output_name}", ["TIME", "SHAPE@"]) as cursor:
    for node in reachability_map:
        print(node)
        cursor.insertRow([reachability_map[node], arcpy.PointGeometry(arcpy.Point(node.split(",")[0], node.split(",")[1]), spatial_reference)])