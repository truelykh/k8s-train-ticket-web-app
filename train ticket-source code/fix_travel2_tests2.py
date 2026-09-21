import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel2-service/src/test/java/travel2/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # We must differentiate basicservice (which returns TravelResult) and seatservice (which returns Integer)
    # Both use HttpMethod.POST and ParameterizedTypeReference in ts-travel2-service!
    bad_mock1 = """        Response<Integer> response5 = new Response<>(1, "Success", 10);
        org.springframework.http.ResponseEntity<Response<Integer>> re5 = new org.springframework.http.ResponseEntity<>(response5, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
                
    good_mock1 = """        Response<Integer> response5 = new Response<>(1, "Success", 10);
        org.springframework.http.ResponseEntity<Response<Integer>> re5 = new org.springframework.http.ResponseEntity<>(response5, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("seatservice"),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
                
    content = content.replace(bad_mock1, good_mock1)
    
    bad_mock2 = """        Response response3 = new Response(1, "Success", travelResult);
        org.springframework.http.ResponseEntity<Response> re3 = new org.springframework.http.ResponseEntity<>(response3, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re3);"""
                
    good_mock2 = """        Response response3 = new Response(1, "Success", travelResult);
        org.springframework.http.ResponseEntity<Response> re3 = new org.springframework.http.ResponseEntity<>(response3, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("basicservice"),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re3);"""
                
    content = content.replace(bad_mock2, good_mock2)

    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
