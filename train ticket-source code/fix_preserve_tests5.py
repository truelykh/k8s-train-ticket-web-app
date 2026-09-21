import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-service/src/test/java/preserve/service/PreserveServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the NPE caused by missing Route and TrainType in TravelResult
    bad_travel_result = """        TravelResult travelResult = new TravelResult();
        travelResult.setPrices( new HashMap<String, String>(){{ put("confortClass", "1.0"); }} );
        Response<TravelResult> response5 = new Response<>(1, null, travelResult);"""
        
    good_travel_result = """        TravelResult travelResult = new TravelResult();
        travelResult.setPrices( new HashMap<String, String>(){{ put("confortClass", "1.0"); put("economyClass", "1.0"); }} );
        Route route = new Route();
        route.setStations(new java.util.ArrayList<>());
        travelResult.setRoute(route);
        TrainType trainType = new TrainType();
        trainType.setConfortClass(100);
        trainType.setEconomyClass(100);
        travelResult.setTrainType(trainType);
        Response<TravelResult> response5 = new Response<>(1, null, travelResult);"""
    
    content = content.replace(bad_travel_result, good_travel_result)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveServiceImplTest in {service_filepath}")
