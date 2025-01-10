from neo4j import GraphDatabase
import geopandas as gpd
driver = GraphDatabase.driver("neo4j+s://260dfa0b.databases.neo4j.io", auth=("neo4j","4xELGnGYvcUlQ-lcwOeqPPv_O1sgDuAHFUMFpJMLzZA"))
session = driver.session()
# query = 'CREATE (m:Miasto {nazwa:"Warszawa"}) RETURN m;'
# session.run(query)
# session.close()

shp = "C:\studia\sem5\Pag\skjz\direction_calosc_0.shp"
gdf = gpd.read_file(shp)
print(gdf.head())

road_classes_speed = {
    "A": 140,
    "S": 120,
    "GP": 100,
    "G": 80,
    "Z": 60,
    "L": 50,
    "D": 40,
    "I": 30,
}

for key in road_classes_speed:
    road_classes_speed[key] /= 2
    
with driver.session() as session:
    for idx,row in gdf.iterrows():
        length = row.geometry.length
        coords = list(row.geometry.coords)
        startPoint = coords[0]
        endPoint = coords[-1]
        x1 = startPoint[0]
        y1 = startPoint[1]
        x2 = endPoint[0]
        y2 = endPoint[1]
        
        edge_id = idx
        length = row.geometry.length
        road_class_speed = road_classes_speed[row['klasaDrogi']]
        time = length/(road_class_speed * 1000 / 3600)
        direction = row['kierunek']
        
        query = f"""
            CREATE (n:Node {{id:'{str(int(x1))+","+str(int(y1))}', location:point({{x:{x1}, y: {y1}}})}})
            WITH n
            CREATE (m:Node {{id:'{str(int(x2))+","+str(int(y2))}', location:point({{x:{x2}, y: {y2}}})}})
            WITH n, m
            """
        
        if direction == "0":
            query += f'create (n)-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time{time}}}]-(m);'
        elif direction == "1":
            query += f'create (n)-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time{time}}}]->(m);'
        elif direction == "2":
            query += f'create (n)<-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time{time}}}]-(m);'
        
        query += " RETURN n, m;"
        session.run(query)
        

session.close()