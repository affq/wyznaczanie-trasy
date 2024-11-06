import arcpy
import os
from klasy import Wierzcholek, Krawedz, Graf
from func import *

#arcpy.env.workspace ="C:\studia\sem5\Pag\pag\pag.gdb"

#fc = "skjz\L4_1_BDOT10k__OT_SKJZ_L.shp"
fc="4krawedzie.shp"

graf = Graf()

with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@', 'klasaDrogi', 'kierunek']) as cursor:
    for row in cursor:
        startPoint = row[1].firstPoint
        endPoint = row[1].lastPoint

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

        start = Wierzcholek(start_id, x1, y1)
        end = Wierzcholek(end_id, x2, y2)
        edge = Krawedz(edge_id, start, end, length, road_class, direction)
        graf.add_edge(edge)

for node in graf.nodes.values():
   print(node.id, node.edges)
   
start_id = next(iter(graf.nodes))
end_id = next(reversed(graf.nodes))
came_from, cost_so_far = dijkstra(graf, start_id, end_id)
#print(f"start_id: {start_id}, end_id: {end_id}\n came_from: {came_from} \n cost: {cost_so_far}")
path = retrieve_path2(came_from, start_id, end_id)
#print(f"path{path}")