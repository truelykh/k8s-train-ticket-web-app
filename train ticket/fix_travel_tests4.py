import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # We must populate all fields accessed by getTickets() in TravelServiceImpl
    bad_mock = """        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
        edu.fudan.common.entity.Route trRoute = new edu.fudan.common.entity.Route();
        trRoute.setStations(new java.util.ArrayList<>());
        travelResult.setRoute(trRoute);
        edu.fudan.common.entity.TrainType trTrainType = new edu.fudan.common.entity.TrainType();
        travelResult.setTrainType(trTrainType);
        
        Response response3 = new Response(1, "Success", travelResult);"""
                
    good_mock = """        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
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
        
        Response response3 = new Response(1, "Success", travelResult);"""
    
    content = content.replace(bad_mock, good_mock)
    
    # We must also set the startTime on the trip!
    bad_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        Mockito.when(repository.findByTripId(Mockito.any(TripId.class))).thenReturn(trip);"""
        
    good_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        trip.setStartTime("2030-01-01 00:00:00");
        Mockito.when(repository.findByTripId(Mockito.any(TripId.class))).thenReturn(trip);"""
        
    content = content.replace(bad_trip_mock, good_trip_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
