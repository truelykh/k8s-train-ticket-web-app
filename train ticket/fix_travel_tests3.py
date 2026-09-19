import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix testGetTripAllDetailInfo NPE caused by empty TravelResult
    bad_mock = """        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
        Response response3 = new Response(1, "Success", travelResult);"""
                
    good_mock = """        edu.fudan.common.entity.TravelResult travelResult = new edu.fudan.common.entity.TravelResult();
        edu.fudan.common.entity.Route trRoute = new edu.fudan.common.entity.Route();
        trRoute.setStations(new java.util.ArrayList<>());
        travelResult.setRoute(trRoute);
        edu.fudan.common.entity.TrainType trTrainType = new edu.fudan.common.entity.TrainType();
        travelResult.setTrainType(trTrainType);
        
        Response response3 = new Response(1, "Success", travelResult);"""
    
    content = content.replace(bad_mock, good_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
