import arcpy
import os
arcpy.env.workspace ="C:\studia\sem5\Pag\pag\pag.gdb"

fc = "C:\studia\sem5\Pag\L4_1_BDOT10k__OT_SKJZ_L.shp"

with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as cursor:
    for row in cursor:
        print(f'Id: {row[0]} xy: {row[1]}')