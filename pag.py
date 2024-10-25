import arcpy
import os
from klasy import Node, Edge, Graf

arcpy.env.workspace ="C:\studia\sem5\Pag\pag\pag.gdb"

fc = "C:\studia\sem5\Pag\L4_1_BDOT10k__OT_SKJZ_L.shp"


with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as cursor:
    for row in cursor:
        
        # poczatek i koniec odcinka jezdni
        startPoint = row[1].firstPoint
        endPoint = row[1].lastPoint
        
        #wsp x,y veretxow
        x1 = startPoint.X
        y1 = startPoint.Y
        x2 = endPoint.X
        y2 = endPoint.Y
        
        #długość odcinka
        length = row[1].length