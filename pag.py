import arcpy
import os
from klasy import Wierzcholek, Krawedz, Graf

arcpy.env.workspace ="C:\studia\sem5\Pag\pag\pag.gdb"

fc = "C:\studia\sem5\Pag\L4_1_BDOT10k__OT_SKJZ_L.shp"

graf = Graf()

with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as cursor:
    for row in cursor:
        startPoint = row[1].firstPoint
        endPoint = row[1].lastPoint
        
        x1 = startPoint.X
        y1 = startPoint.Y
        x2 = endPoint.X
        y2 = endPoint.Y

        #długość odcinka
        length = row[1].length

        #id do edge?
        edge_id = '?????????????'
        #klasa drogi?
        road_class = '?????????????'
        #kierunkowość drogi?
        direction = '?????????????'

        start = Wierzcholek(str(x1) + ", " + str(y1), x1, y1)
        end = Wierzcholek(str(x2) + ", " + str(y2), x2, y2)
        edge = Krawedz(edge_id, start, end, length, road_class, direction)
        graf.add_edge(edge)

#print(graf.nodes)
#print(graf.edges)
