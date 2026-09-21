import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-service/src/test/java/preserve/service/PreserveServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix testDipatchSeat
    bad_seat = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                HttpMethod.POST,
                requestEntityTicket,
                new ParameterizedTypeReference<Response<Ticket>>() {
                })).thenReturn(reTicket);"""
    
    good_seat = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(reTicket);"""
    content = content.replace(bad_seat, good_seat)
    
    # Fix testGetAccount
    bad_account = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<Response<User>>() {
                })).thenReturn(re);"""
                
    good_account = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re);"""
    content = content.replace(bad_account, good_account)

    # Fix testPreserve (chained mocks)
    bad_preserve_mock = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re2).thenReturn(re3).thenReturn(re4).thenReturn(re4).thenReturn(re5).thenReturn(re6).thenReturn(re7).thenReturn(re9);"""
                
    good_preserve_mock = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("contactservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re2);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("travelservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re3);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("seatservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re6);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("orderservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re7);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re9);"""
    
    content = content.replace(bad_preserve_mock, good_preserve_mock)
    
    # We must also ensure the TravelResult mock (re5) doesn't conflict, but it's not even used now.
    
    # Wait, testPreserve also expects `re1` for checkSecurity, createFoodOrder, createConsign, addAssuranceForOrder.
    # The existing Class.class mock handles this perfectly:
    # Mockito.when(restTemplate.exchange(Mockito.anyString(), Mockito.any(HttpMethod.class), Mockito.any(HttpEntity.class), Mockito.any(Class.class))).thenReturn(re1).thenReturn(re1).thenReturn(re1).thenReturn(re1).thenReturn(re10);
    # Actually wait, testPreserve uses .thenReturn(re1).thenReturn(re1).thenReturn(re1).thenReturn(re1).thenReturn(re10);
    # That is fine.
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveServiceImplTest in {service_filepath}")
