import os
import re

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-train-service/src/test/java/train/service/TrainServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix TrainType trainType = new TrainType(); to avoid null names and ids
    content = content.replace("TrainType trainType = new TrainType();\n", "TrainType trainType = new TrainType();\n        trainType.setId(\"train-id\");\n        trainType.setName(\"train-name\");\n")
    
    # Fix testCreate2: findByName should be mocked instead of findById
    content = content.replace("Mockito.when(repository.findById(Mockito.anyString())).thenReturn(java.util.Optional.ofNullable(trainType));\n        boolean result = trainServiceImpl.create(trainType, headers);",
                              "Mockito.when(repository.findByName(Mockito.anyString())).thenReturn(trainType);\n        boolean result = trainServiceImpl.create(trainType, headers);")
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed TrainServiceImplTest in {service_filepath}")
