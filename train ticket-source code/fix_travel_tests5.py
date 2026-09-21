import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # We must set tripId on the trip to avoid NPE on trip.getTripId().toString()
    bad_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        trip.setStartTime("2030-01-01 00:00:00");"""
        
    good_trip_mock = """        Trip trip = new Trip();
        trip.setRouteId("route_id");
        trip.setStartTime("2030-01-01 00:00:00");
        trip.setTripId(new TripId("trip_id"));"""
        
    content = content.replace(bad_trip_mock, good_trip_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
