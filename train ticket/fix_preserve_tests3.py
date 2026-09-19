import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-service/src/test/java/preserve/service/PreserveServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # We missed basicservice mock in testPreserve!
    bad_preserve_mock = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re9);"""
                
    good_preserve_mock = """        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re9);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("basicservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(HttpEntity.class),
                org.mockito.ArgumentMatchers.any(ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
    
    content = content.replace(bad_preserve_mock, good_preserve_mock)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveServiceImplTest in {service_filepath}")
