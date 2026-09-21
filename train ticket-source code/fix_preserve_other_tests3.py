import os
import re

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-other-service/src/test/java/preserveOther/service/PreserveOtherServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # 5. Fix testPreserve (chained mocks) - Use regex to match the exact block to avoid minor differences
    pattern = r'Mockito\.when\(restTemplate\.exchange\(\s*Mockito\.anyString\(\),\s*Mockito\.any\(HttpMethod\.class\),\s*Mockito\.any\(HttpEntity\.class\),\s*Mockito\.any\(ParameterizedTypeReference\.class\)\)\)\s*\.thenReturn\(re2\).*?thenReturn\(re9\);'
    
    good_preserve_mock = """Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("contactservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re2);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("travel2service"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re3);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("seatservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re6);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("orderOtherService"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re7);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re9);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("basicservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re5);"""
    
    new_content, count = re.subn(pattern, good_preserve_mock, content, flags=re.DOTALL)
    print(f"Replaced {count} instances of chained mocks")
    
    with open(service_filepath, 'w') as f:
        f.write(new_content)
    print(f"Fixed PreserveOtherServiceImplTest in {service_filepath}")
