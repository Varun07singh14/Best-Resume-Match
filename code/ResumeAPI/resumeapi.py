from flask import  Flask, jsonify, request
import accessFiles

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predictResumes():
    if (request.data and request.get_json()!={}):
        instance =request.get_json().get('instances');
        mlEvaluateRequest = request.get_json().get('parameters');
        if "context" in mlEvaluateRequest and "category" in mlEvaluateRequest and "threshold" in mlEvaluateRequest and "noOfmatches" in mlEvaluateRequest and "inputPath" in mlEvaluateRequest:
        #Logic to integrate the ML Model to fetch the data  
            bucket_name =  accessFiles.Extract_Bucket_Name_From_Input_Path(mlEvaluateRequest["inputPath"])
            scores = accessFiles.verify_Access_To_Cloud_Storage_And_Return_Files(bucket_name, mlEvaluateRequest)
            return jsonify({"predictions":scores})
        else:
            return jsonify({"error": "Search critieria parameters are missing",}), 401
    else:
        return jsonify({"error":"Search critieria is missing"}),404

@app.route('/health')
def health():
    return "OK"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=False)