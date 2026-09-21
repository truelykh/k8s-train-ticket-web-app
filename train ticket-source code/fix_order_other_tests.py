import os

# Fix OrderOtherControllerTest
controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-other-service/src/test/java/other/controller/OrderOtherControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    # OrderInfo qi = new OrderInfo();
    content = content.replace("OrderInfo qi = new OrderInfo();\n", "OrderInfo qi = new OrderInfo();\n        qi.setLoginId(\"login-id\");\n")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed OrderOtherControllerTest in {controller_filepath}")

# Fix OrderOtherServiceImplTest
service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-other-service/src/test/java/other/service/OrderOtherServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the Ribbon load balancer port removal issue in mock URLs
    content = content.replace("http://ts-station-service:12345/api/v1/stationservice/stations/namelist", 
                              "http://ts-station-service/api/v1/stationservice/stations/namelist")
    content = content.replace("http://ts-station-service:12345", "http://ts-station-service")
    
    # Replace save(Mockito.any(Order.class)) mock from null to the argument
    content = content.replace("Mockito.when(orderRepository.save(Mockito.any(Order.class))).thenReturn(null);", 
                              "Mockito.when(orderRepository.save(Mockito.any(Order.class))).thenAnswer(i -> i.getArguments()[0]);")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed OrderOtherServiceImplTest in {service_filepath}")
