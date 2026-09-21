import os
import re

files_to_fix = [
    "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-service/src/test/java/order/service/OrderServiceImplTest.java",
    "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-other-service/src/test/java/other/service/OrderOtherServiceImplTest.java"
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # In test methods, we create Order order = new Order();
        # We need to set an account ID so that it doesn't cause Mockito null matching issues
        content = content.replace("Order order = new Order();\n", "Order order = new Order();\n        order.setAccountId(\"account-id\");\n")
        
        # For testDeleteOrder1 and testDeleteOrder2:
        # Assert.assertEquals(new Response<>(1, "Delete Order Success", order), result);
        # -> Response data for delete is orderUuid string! But wait, in OrderServiceImpl:
        # return new Response<>(1, "Delete Order Success", order);
        # So it does return the Order object in ts-order-service!
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed accountIds in {filepath}")

# Let's also fix the OrderControllerTest.java issue
controller_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-service/src/test/java/order/controller/OrderControllerTest.java"
if os.path.exists(controller_filepath):
    with open(controller_filepath, 'r') as f:
        content = f.read()
    
    # OrderInfo qi = new OrderInfo();
    content = content.replace("OrderInfo qi = new OrderInfo();\n", "OrderInfo qi = new OrderInfo();\n        qi.setLoginId(\"login-id\");\n")
    
    with open(controller_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed OrderControllerTest in {controller_filepath}")

