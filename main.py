import arcpy
from klasy import Wierzcholek, Krawedz, Graf
from func import a_star, retrieve_path

arcpy.env.overwriteOutput = True

fc = "skjz\direction_calosc_0.shp"
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

with open('nodes.txt', 'w') as f:
    for node in graf.nodes.values():
        f.write(f"{node.id}\n")
   
start_point = graf.snap(474638, 572636)
end_point = graf.snap(471582, 576616)

came_from, cost_so_far = a_star(graf, start_point, end_point,'distance')
length_a_star = cost_so_far[end_point.id]
path = retrieve_path(came_from, start_point.id, end_point.id)

#----------wizualizacja----------------
spatial_reference = arcpy.Describe(fc).spatialReference

output_folder= "shp"
output_name = "path.shp"
arcpy.management.CreateFeatureclass(output_folder, output_name, "POLYLINE",spatial_reference=spatial_reference)
arcpy.AddField_management(f"{output_folder}/{output_name}", "NR", "FLOAT")

edges_list = []
for i in range(len(path)-1):
    start_node = path[i] 
    end_node = path[i + 1] 
    found_edge = False
    
    for edge in graf.edges.values():
        if (edge.from_node.id == start_node and edge.to_node.id == end_node) or (edge.from_node.id == end_node and edge.to_node.id == start_node):
            edges_list.append(edge)
            found_edge = True
            break
    if not found_edge:
        print(f"Nie znaleziono krawędzi między {start_node} i {end_node}")
        break
    
with arcpy.da.InsertCursor(f"{output_folder}/{output_name}", ["NR", "SHAPE@"]) as cursor:
    for i, edge in enumerate(edges_list):
        print(edge)
        geometry = arcpy.FromWKT(edge.wkt)
        cursor.insertRow([i, geometry])

print("SHP done")