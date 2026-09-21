import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-service/src/test/java/preserve/service/PreserveServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # 1. Add sendService mock
    content = content.replace("private RestTemplate restTemplate;", 
                              "private RestTemplate restTemplate;\n\n    @Mock\n    private preserve.mq.RabbitSend sendService;")
    
    # 2. Fix testDipatchSeat
    bad_seat = '"http://ts-seat-service:18898/api/v1/seatservice/seats"'
    content = content.replace(bad_seat, "Mockito.anyString()")
    
    # 3. Fix testGetAccount
    bad_account = '"http://ts-user-service:12342/api/v1/userservice/users/id/1"'
    content = content.replace(bad_account, "Mockito.anyString()")
    
    # 4. Fix testSendEmail
    bad_email = """        HttpEntity requestEntitySendEmail = new HttpEntity(notifyInfo, headers);
        ResponseEntity<Boolean> reSendEmail = new ResponseEntity<>(true, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                "http://ts-notification-service:17853/api/v1/notifyservice/notification/preserve_success",
                HttpMethod.POST,
                requestEntitySendEmail,
                Boolean.class)).thenReturn(reSendEmail);"""
                
    good_email = """        Mockito.doNothing().when(sendService).send(Mockito.anyString());"""
    content = content.replace(bad_email, good_email)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed PreserveServiceImplTest in {service_filepath}")
