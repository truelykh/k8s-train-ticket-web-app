import os

service_filepath = "/Users/rakesh/Dev/Projects/train ticket web app/train ticket/ts-preserve-other-service/src/test/java/preserveOther/service/PreserveOtherServiceImplTest.java"
if os.path.exists(service_filepath):
    with open(service_filepath, 'r') as f:
        content = f.read()
    
    # Fix the package names for Route and TrainType
    bad_route = "preserveOther.entity.Route"
    good_route = "edu.fudan.common.entity.Route"
    content = content.replace(bad_route, good_route)
    
    bad_train_type = "preserveOther.entity.TrainType"
    good_train_type = "edu.fudan.common.entity.TrainType"
    content = content.replace(bad_train_type, good_train_type)
    
    with open(service_filepath, 'w') as f:
        f.write(content)
    print(f"Fixed package names in {service_filepath}")
