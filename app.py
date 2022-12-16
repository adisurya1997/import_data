import json
import os
import requests
from sys import stderr
from flask import Flask, request, jsonify,make_response

app = Flask(__name__)

api_key = os.environ.get("API_KEY", "")
if api_key == "":
    print("api key is required", file=stderr)

api_base_url = "https://api.stagingv3.microgen.id/query/api/v1/" + api_key

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.post("/api/create/sourcecode")
def sourcecode():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        request_data = request.get_json()
        database = request_data['database']
        table = request_data['table']
        path_file = request_data['path_file']
        name = request_data['name']
        if not database:
            return jsonify({"msg": "Missing database parameter"}), 400
        if not table:
            return jsonify({"msg": "Missing table parameter"}), 400
        if not path_file:
            return jsonify({"msg": "Missing path_file parameter"}), 400
        if not name:
            return jsonify({"msg": "Missing name parameter"}), 400
        try:
            url = 'https://ezpdlqrjcm.function.microgen.id/api/login'
            response1 = requests.post(url,data={'username': 'admin', 'password':'admin'})
            source = str(response1.json()["Set-Cookie"])
            try:
                url = 'https://ezpdlqrjcm.function.microgen.id/api/createnote?'+source+''
                response2 = requests.post(url,json={"name":str(name)})
                data = response2.json()
                sdata = str(data["body"])
                try:
                    text = "%jdbc(hive)\nLOAD DATA INPATH '"+path_file+"' INTO TABLE "+database+"."+table+"\n"
                    url2 = 'https://ezpdlqrjcm.function.microgen.id/api/notebook/'+sdata+'/paragraph'
                    response3 = requests.post(url2,json={"title": "Paragraph insert revised","text":text })
                    url = "https://sapujagad.id/sjnotebook/"+sdata+""
                    my_dict = {}
                    my_dict['Url']= url
                    xs = make_response(my_dict)
                    return xs
                except:
                    return jsonify({"msg": "Missing create paragraph code"}), 400
            except:
                return jsonify({"msg": "Missing create note"}), 400
        except:
            return jsonify({"msg": "Missing Authorization"}), 401
    except:
        return jsonify({"msg": "error server"}), 500

if __name__ == "__main__":
    app.run(debug=True)
