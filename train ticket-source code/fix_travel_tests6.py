import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # "trip_id" is not a valid train type (must start with G, D, T, K, or Z)
    # TripId constructor leaves type as null if it doesn't match, throwing NPE on toString()
    content = content.replace("new TripId(\"trip_id\")", "new TripId(\"G1234\")")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
