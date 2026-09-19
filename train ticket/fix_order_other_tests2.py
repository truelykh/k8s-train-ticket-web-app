import os

# Fix OrderOtherControllerTest
controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-other-service/src/test/java/other/controller/OrderOtherControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    # QueryInfo qi = new QueryInfo();
    content = content.replace("QueryInfo qi = new QueryInfo();\n", "QueryInfo qi = new QueryInfo();\n        qi.setLoginId(\"login-id\");\n")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed OrderOtherControllerTest in {controller_filepath}")

# Fix OrderOtherServiceImplTest
service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-other-service/src/test/java/other/service/OrderOtherServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Replace save(Mockito.any(Order.class)) mock from null to the argument for orderOtherRepository
    content = content.replace("Mockito.when(orderOtherRepository.save(Mockito.any(Order.class))).thenReturn(null);", 
                              "Mockito.when(orderOtherRepository.save(Mockito.any(Order.class))).thenAnswer(i -> i.getArguments()[0]);")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed OrderOtherServiceImplTest in {service_filepath}")
