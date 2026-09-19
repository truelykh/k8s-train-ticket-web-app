import os
import re

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-station-service/src/test/java/fdse/microservice/service/StationServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix Station station = new Station();
    content = content.replace("Station station = new Station();\n", "Station station = new Station();\n        station.setId(\"station-id\");\n        station.setName(\"station-name\");\n")
    
    # Fix Station info = new Station();
    content = content.replace("Station info = new Station();\n", "Station info = new Station();\n        info.setId(\"station-id\");\n        info.setName(\"station-name\");\n")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed StationServiceImplTest in {service_filepath}")
