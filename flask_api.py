from flask import Flask, request, jsonify
import json
import create_qr as cq
from waitress import serve
import pyaes
app = Flask(__name__)


plaintext = b'secret data'
key=b'1234567890123456'
aes = pyaes.AESModeOfOperationCTR(key)    
ciphertext = aes.encrypt(plaintext)

# show the encrypted data
print (ciphertext)

# DECRYPTION
# CRT mode decryption requires a new instance be created
aes = pyaes.AESModeOfOperationCTR(key)

# decrypted data is always binary, need to decode to plaintext
decrypted = aes.decrypt(ciphertext).decode('utf-8')

# True
print (decrypted == plaintext)
print (plaintext)

@app.route("/api/v1/get_qr", methods=["GET", "POST"])
def get_qr():
    print(request.method)
    try:
        data = request.args
        pk = data["pk"]
        if(not pk):
            obj={"error":1,"message":"KEY IS EMPTY","status":500}
            return jsonify(obj), 500
        qr_code = cq.get_qr_url(pk)
        if(qr_code==False):
            obj={"error":1,"message":"Error Generating qr try again","status":403}
            return jsonify(obj), 403
        obj={"error":0,"message":"QR generated successfully","status":200,"qr_code":qr_code}
        return jsonify(obj),200
    except Exception as e:
        obj={"error":1,"message":"KEY NOT FOUND","status":500}
        return jsonify(obj), 500
    


@app.route("/api/v1/get_policy", methods=["GET", "POST"])
def get_policy():
    print(request.method)
    try:
        data = request.args
        pk = data["pk"]
        if(not pk):
            obj={"error":1,"message":"KEY IS EMPTY","status":500}
            return jsonify(obj), 500
        policy = cq.get_policy(pk)
        if(policy==False):
            obj={"error":1,"message":"No Policy found for given Policy name","status":403}
            return jsonify(obj), 403
        obj={"error":0,"message":"Policy fetched successfully","status":200,"policy":policy}
        return jsonify(obj),200
       
    except Exception as e:
        obj={"error":1,"message":"KEY NOT FOUND","status":500}
        return jsonify(obj), 500


@app.route("/api/v1/update_policy", methods=[ "POST"])
def update_policy():
    print(request.method)
    try:
        data = request.args
        # print(request.json)
        body=request.get_json()
        print(body)
        if(not body):
            obj={"error":1,"message":"BODY IS EMPTY","status":500}
            return jsonify(obj), 500
        pk = data["pk"]
        if(not pk):
            obj={"error":1,"message":"KEY IS EMPTY","status":500}
            return jsonify(obj), 500
        new_policy_json =body

        if not all([pk, new_policy_json]):
            obj={"error":1,"message":"Both pk and new_policy_json are required","status":500}
            return jsonify(obj), 500
        
        try:
            policy = cq.update_policy(pk=pk, new_policy_json=new_policy_json)
            obj={"error":0,"message":"Policy updated successfully","status":200}
            
            return jsonify(obj),200
        except Exception as e:
            obj={"error":1,"message":"Not able to update Policy",e:e,"status":500}
            return jsonify(obj), 500
    except Exception as e:
        obj={"error":1,"message":"Error Occured","status":500}
        return jsonify(obj), 500

@app.route("/api/v1/release_device", methods=[ "GET", "POST"])
def release_device():
    try:
        data = request.args
        pk = data["pk"]
        print(pk)
        
        if(not pk):
            obj={"error":1,"message":"KEY IS EMPTY","status":500}
            return jsonify(obj), 500
    
        
        try:
            policy = cq.release_device(pk=pk)
            if(policy==False):
                obj={"error":1,"message":"No Policy found for given Policy name","status":403}
                return jsonify(obj), 403
            obj={"error":0,"message":"Policy updated successfully","status":200}
            return jsonify(obj),200
        except Exception as e:
            obj={"error":1,"message":"Not able to update Policy",e:e,"status":500}
            return jsonify(obj), 500
    except Exception as e:
        obj={"error":1,"message":"Some error occured","status":500}
        return jsonify(obj), 500



@app.route("/", methods=["GET", "POST"])
def say_hi():
    obj={"error":0,"message":"API WORKING","status":200}
    return jsonify(obj), 200


if __name__ == "__main__":
    serve(app,host="0.0.0.0", port=5001,threads=4)
    # app.run(threaded=True,debug=False, host="0.0.0.0", port=5001)
