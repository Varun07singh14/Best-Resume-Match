import functions_framework
from flask import  Flask, jsonify, request
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from flask_cors import cross_origin

@functions_framework.http
@cross_origin(allowed_methods=['POST'])
def predict_custom_trained_model_sample(request):
    
    api_endpoint: str = "us-central1-aiplatform.googleapis.com"
    location: str = "us-central1"
    endpoint_id: str = "6147266156802605056" 
    project: str = "847355328557"

    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instancesDict = { "instance": "us-cental"}
    instances = [json_format.ParseDict(instancesDict, Value())]
    request_json=request.get_json(silent=True)
    parameters_dict = {
    "context": request_json["context"],
    "category": request_json["category"],
    "threshold":  request_json["threshold"],
    "noOfmatches": request_json["noOfmatches"],
    "inputPath":  request_json["inputPath"],
    }
    
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    
    # print(" deployed_model_id:", response.deployed_model_id)
    #print(response)
    
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    # return json_format.ParseDict(response.predictions,Value()) 
    resultPredictions =[]
    if "predictions" in response :
        predictions = response.predictions
        for prediction in predictions:
            resultPredictions.append(dict(prediction))

    return jsonify({"predictions":resultPredictions})