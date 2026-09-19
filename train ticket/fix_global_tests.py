import os
import re

search_path = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket"

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith("Test.java"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern 1: Mockito.when(repository.findById(Mockito.anyString()).get()).thenReturn(trainType);
            # Replace with: Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.ofNullable(trainType));
            content = re.sub(r'Mockito\.when\(([a-zA-Z0-9_]+)\.findById\(Mockito\.anyString\(\)\)\.get\(\)\)\.thenReturn\((.*?)\);', 
                             r'Mockito.when(\1.findById(Mockito.anyString())).thenReturn(java.util.Optional.ofNullable(\2));', 
                             content)
                             
            # Pattern 2: Mockito.when(repository.findById(Mockito.anyString())).thenReturn(null);
            # Replace with: Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.empty());
            content = re.sub(r'Mockito\.when\(([a-zA-Z0-9_]+)\.findById\(Mockito\.anyString\(\)\)\)\.thenReturn\(null\);', 
                             r'Mockito.when(\1.findById(Mockito.anyString())).thenReturn(java.util.Optional.empty());', 
                             content)
                             
            if original_content != content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed {filepath}")
