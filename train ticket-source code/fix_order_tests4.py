import os

filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-order-service/src/test/java/order/service/OrderServiceImplTest.java"

if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Revert my bad global replace
    content = content.replace(".thenAnswer(i -> i.getArguments()[0]);", ".thenReturn(null);")
    
    # Only replace for save(Mockito.any(Order.class))
    content = content.replace("Mockito.when(orderRepository.save(Mockito.any(Order.class))).thenReturn(null);", 
                              "Mockito.when(orderRepository.save(Mockito.any(Order.class))).thenAnswer(i -> i.getArguments()[0]);")
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")
