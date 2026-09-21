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
        
        # Fix Optional.get() stubbing issue:
        # Mockito.when(orderRepository.findById(Mockito.any(String.class)).get()).thenReturn(order); ->
        # Mockito.when(orderRepository.findById(Mockito.any())).thenReturn(java.util.Optional.of(order));
        content = re.sub(
            r'Mockito\.when\((\w+\.findById\(.*?\))\.get\(\)\)\.thenReturn\((\w+)\);',
            r'Mockito.when(\1).thenReturn(java.util.Optional.of(\2));',
            content
        )
        
        # Also fix .findById returning null incorrectly instead of Optional.empty()
        # Mockito.when(orderRepository.findById(Mockito.any(String.class))).thenReturn(null); ->
        # Mockito.when(orderRepository.findById(Mockito.any())).thenReturn(java.util.Optional.empty());
        content = re.sub(
            r'Mockito\.when\((\w+\.findById\(.*?\))\)\.thenReturn\(null\);',
            r'Mockito.when(\1).thenReturn(java.util.Optional.empty());',
            content
        )
        
        # Replace Mockito.any(String.class) with Mockito.any()
        content = content.replace("Mockito.any(String.class)", "Mockito.any()")
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
