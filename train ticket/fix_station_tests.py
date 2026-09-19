import os

# Fix StationControllerTest
controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-station-service/src/test/java/fdse/microservice/controller/StationControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    # Fix 405 Method Not Allowed in DELETE test
    content = content.replace("MockMvcRequestBuilders.delete(\"/api/v1/stationservice/stations\")", 
                              "MockMvcRequestBuilders.delete(\"/api/v1/stationservice/stations/station-id\")")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed StationControllerTest in {controller_filepath}")

# Fix StationServiceImplTest
service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-station-service/src/test/java/fdse/microservice/service/StationServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the .get() NoSuchElementException Mockito bugs and NullPointerException bugs
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString()).get()).thenReturn(null);", 
                              "Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.empty());")
    
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString())).thenReturn(null);", 
                              "Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.empty());")
    
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString()).get()).thenReturn(station);", 
                              "Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.of(station));")
    
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString()).get()).thenReturn(info);", 
                              "Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.of(info));")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed StationServiceImplTest in {service_filepath}")
