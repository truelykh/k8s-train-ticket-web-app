import os

controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel2-service/src/test/java/travel2/controller/TravelControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    content = content.replace("Mockito.when(service.query(Mockito.any(TripInfo.class)", 
                              "Mockito.when(service.queryByBatch(Mockito.any(TripInfo.class)")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelControllerTest in {controller_filepath}")

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel2-service/src/test/java/travel2/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the past date logic
    content = content.replace("System.currentTimeMillis() - 86400000", "System.currentTimeMillis() + 86400000")
    
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
    
    # Fix testGetTripAllDetailInfo mocking two restTemplate.exchange calls with the same any(HttpMethod.class)
    bad_mock2 = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re2);"""
                
    good_mock2 = """        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.GET),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re2);
        
        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
        edu.fudan.common.entity.Route trRoute = new edu.fudan.common.entity.Route();
        java.util.List<String> stations = new java.util.ArrayList<>();
        stations.add("from_station");
        stations.add("to_station");
        stations.add("startPlace");
        stations.add("endPlace");
        trRoute.setStations(stations);
        java.util.List<Integer> distances = new java.util.ArrayList<>();
        distances.add(0);
        distances.add(100);
        distances.add(100);
        distances.add(100);
        trRoute.setDistances(distances);
        travelResult.setRoute(trRoute);
        edu.fudan.common.entity.TrainType trTrainType = new edu.fudan.common.entity.TrainType();
        trTrainType.setAverageSpeed(100);
        trTrainType.setConfortClass(10);
        trTrainType.setEconomyClass(10);
        travelResult.setTrainType(trTrainType);
        java.util.Map<String, String> prices = new java.util.HashMap<>();
        prices.put("confortClass", "100.0");
        prices.put("economyClass", "50.0");
        travelResult.setPrices(prices);
        
        Response response3 = new Response(1, "Success", travelResult);
        org.springframework.http.ResponseEntity<Response> re3 = new org.springframework.http.ResponseEntity<>(response3, org.springframework.http.HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re3);"""
    
    content = content.replace(bad_mock2, good_mock2)

    # We must also set the startTime and TripId on the trip!
    bad_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        Mockito.when(repository.findByTripId(Mockito.any(TripId.class))).thenReturn(trip);"""
        
    good_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        trip.setStartTime("2030-01-01 00:00:00");
        trip.setTripId(new TripId("G1234"));
        Mockito.when(repository.findByTripId(Mockito.any(TripId.class))).thenReturn(trip);"""
        
    content = content.replace(bad_trip_mock, good_trip_mock)

    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
