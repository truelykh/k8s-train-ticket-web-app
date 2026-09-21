import os

# Fix TravelControllerTest
controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/controller/TravelControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    # Fix testQueryInfo2 mocking the wrong method
    content = content.replace("Mockito.when(service.query(Mockito.any(TripInfo.class), Mockito.any(HttpHeaders.class))).thenReturn(response);", 
                              "Mockito.when(service.queryByBatch(Mockito.any(TripInfo.class), Mockito.any(HttpHeaders.class))).thenReturn(response);")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelControllerTest in {controller_filepath}")

# Fix TravelServiceImplTest
service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix testGetTripAllDetailInfo mocking two restTemplate.exchange calls with the same any(HttpMethod.class)
    bad_mock = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re2);"""
                
    good_mock = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.GET),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re2);
        
        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
        Response response3 = new Response(1, "Success", travelResult);
        org.springframework.http.ResponseEntity<Response> re3 = new org.springframework.http.ResponseEntity<>(response3, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re3);"""
    
    content = content.replace(bad_mock, good_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
