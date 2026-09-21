import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-other-service/src/test/java/preserveOther/service/PreserveOtherServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # 1. Add sendService mock
    content = content.replace("private RestTemplate restTemplate;", 
                              "private RestTemplate restTemplate;\n\n    @Mock\n    private preserveOther.mq.RabbitSend sendService;")
    
    # 2. Fix testDipatchSeat
    bad_seat = """        Mockito.when(restTemplate.exchange(
                "http://ts-seat-service:18898/api/v1/seatservice/seats",
                HttpMethod.POST,
                requestEntityTicket,
                new ParameterizedTypeReference<Response<Ticket>>() {
                })).thenReturn(reTicket);"""
    good_seat = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(reTicket);"""
    content = content.replace(bad_seat, good_seat)
    
    # 3. Fix testGetAccount
    bad_account = """        Mockito.when(restTemplate.exchange(
                "http://ts-user-service:12342/api/v1/userservice/users/id/1",
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<Response<User>>() {
                })).thenReturn(re);"""
    good_account = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re);"""
    content = content.replace(bad_account, good_account)
    
    # 4. Fix testSendEmail
    bad_email = """        HttpEntity requestEntitySendEmail = new HttpEntity(notifyInfo, headers);
        ResponseEntity<Boolean> reSendEmail = new ResponseEntity<>(true, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                "http://ts-notification-service:17853/api/v1/notifyservice/notification/preserve_success",
                HttpMethod.POST,
                requestEntitySendEmail,
                Boolean.class)).thenReturn(reSendEmail);"""
    good_email = """        Mockito.doNothing().when(sendService).send(org.mockito.ArgumentMatchers.anyString());"""
    content = content.replace(bad_email, good_email)

    # 5. Fix testPreserve (chained mocks)
    bad_preserve_mock = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re2).thenReturn(re3).thenReturn(re4).thenReturn(re4).thenReturn(re5).thenReturn(re6).thenReturn(re7).thenReturn(re9);"""
    good_preserve_mock = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("contactservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re2);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("travel2service"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re3);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("seatservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re6);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("orderOtherService"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re7);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re9);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("basicservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
    content = content.replace(bad_preserve_mock, good_preserve_mock)
    
    # Note: I used "travel2service" for getTripAllDetailInformation, and "orderOtherService" for createOrder!
    # Because it is preserve-OTHER-service, which uses travel2-service and order-other-service!
    
    # 6. Fix the NPE caused by missing Route and TrainType in TravelResult
    bad_travel_result = """        TravelResult travelResult = new TravelResult();
        travelResult.setPrices( new HashMap<String, String>(){{ put("confortClass", "1.0"); }} );
        Response<TravelResult> response5 = new Response<>(null, null, travelResult);"""
    good_travel_result = """        TravelResult travelResult = new TravelResult();
        travelResult.setPrices( new java.util.HashMap<String, String>(){{ put("confortClass", "1.0"); put("economyClass", "1.0"); }} );
        preserveOther.entity.Route route = new preserveOther.entity.Route();
        route.setStations(new java.util.ArrayList<>());
        travelResult.setRoute(route);
        preserveOther.entity.TrainType trainType = new preserveOther.entity.TrainType();
        trainType.setConfortClass(100);
        trainType.setEconomyClass(100);
        travelResult.setTrainType(trainType);
        Response<TravelResult> response5 = new Response<>(1, null, travelResult);"""
    content = content.replace(bad_travel_result, good_travel_result)
    
    # 7. Fix the NPE caused by auto-unboxing null Integer status to int
    content = content.replace("new Response<>(null, null,", "new Response<>(1, null,")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveOtherServiceImplTest in {service_filepath}")
