from neo4j import GraphDatabase
import geopandas as gpd

with open ("neo4j/credentials.txt", "r") as file:
    lines = file.readlines()
    uri = lines[0].strip()
    user = lines[1].strip()
    password = lines[2].strip()

driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session()

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

shp = "skjz\direction_calosc_0.shp"
gdf = gpd.read_file(shp)

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
        
        # query = f"""
        #     CREATE (n:Node {{id: apoc.util.md5([{x1}, {y1}]), location:point({{x:{x1}, y: {y1}}})}})
        #     WITH n
        #     CREATE (m:Node {{id: apoc.util.md5([{x2}, {y2}]), location:point({{x:{x2}, y: {y2}}})}})
        #     WITH n, m
        #     """

        query = f"match (n:Node {{id: apoc.util.md5([{x1}, {y1}])}}), (m:Node {{id: apoc.util.md5([{x2}, {y2}])}})"
        
        if direction == 0:
            query += f'create (n)-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time: {time}}}]-(m);'
        elif direction == 1:
            query += f'create (n)-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time: {time}}}]->(m);'
        elif direction == 2:
            query += f'create (n)<-[:CONNECTED_TO {{edge_id:{edge_id}, length:{length}, time: {time}}}]-(m);'
        query += " RETURN n, m;"
        session.run(query)

session.close()