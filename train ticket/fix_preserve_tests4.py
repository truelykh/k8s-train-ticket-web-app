import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-service/src/test/java/preserve/service/PreserveServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the NPE caused by auto-unboxing null Integer status to int
    content = content.replace("new Response<>(null, null,", "new Response<>(1, null,")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveServiceImplTest in {service_filepath}")
