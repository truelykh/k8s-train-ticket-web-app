import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-station-service/src/test/java/fdse/microservice/service/StationServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix testCreate2: findByName should be mocked instead of findById
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.of(station));\n        Response result = stationServiceImpl.create(station, headers);",
                              "Mockito.when(repository.findByName(Mockito.anyString())).thenReturn(station);\n        Response result = stationServiceImpl.create(station, headers);")
    
    # Fix testQueryById1: The assertion expected "" because the mock didn't have a name. Now it has "station-name".
    content = content.replace("Assert.assertEquals(new Response<>(1, \"Success\", \"\"), result);", 
                              "Assert.assertEquals(new Response<>(1, \"Success\", \"station-name\"), result);")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed StationServiceImplTest in {service_filepath}")
