import os
import re

filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-service/src/test/java/order/service/OrderServiceImplTest.java"

if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix the Ribbon load balancer port removal issue in mock URLs
    content = content.replace("http://ts-station-service:12345/api/v1/stationservice/stations/namelist", 
                              "http://ts-station-service/api/v1/stationservice/stations/namelist")
    content = content.replace("http://ts-station-service:12345", "http://ts-station-service")
    
    # Fix the NPE caused by orderRepository.save returning null
    # Mockito.when(orderRepository.save(Mockito.any(Order.class))).thenReturn(null);
    # Replace with .thenReturn(new Order()) to avoid NPE on order.getId()
    content = content.replace(".thenReturn(null);", ".thenAnswer(i -> i.getArguments()[0]);")
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")
