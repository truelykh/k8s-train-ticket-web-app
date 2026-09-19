import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # queryForStationId should use HttpMethod.GET to not intercept getRestTicketNumber
    bad_mock1 = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re1);"""
                
    good_mock1 = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.GET),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re1);
                
        Response<Integer> response5 = new Response<>(1, "Success", 10);
        org.springframework.http.ResponseEntity<Response<Integer>> re5 = new org.springframework.http.ResponseEntity<>(response5, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
                
    content = content.replace(bad_mock1, good_mock1)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
