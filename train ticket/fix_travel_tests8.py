import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-travel-service/src/test/java/travel/service/TravelServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # We must populate travelResult.prices to avoid NPE
    bad_mock = """        travelResult.setTrainType(trTrainType);
        
        Response response3 = new Response(1, "Success", travelResult);"""
                
    good_mock = """        travelResult.setTrainType(trTrainType);
        java.util.Map<String, String> prices = new java.util.HashMap<>();
        prices.put("confortClass", "100.0");
        prices.put("economyClass", "50.0");
        travelResult.setPrices(prices);
        
        Response response3 = new Response(1, "Success", travelResult);"""
                
    content = content.replace(bad_mock, good_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TravelServiceImplTest in {service_filepath}")
