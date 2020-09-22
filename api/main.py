from flask import Flask,request,jsonify,render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
import io
import requests
from subprocess import call, Popen, PIPE
from array import array
from PIL import Image
import sys
import json
import time


remote_image_handw_text_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"


key = 'ffc60f43d45049b185f8ab5c9b79c2d3'


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(THIS_FOLDER, 'uploads')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploadImage',methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def uploadImage():
    codedatafile = request.files['file']
    if codedatafile:
        filename = secure_filename(codedatafile.filename)
        codedatafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        response = sendRequest(filepath)
        time.sleep(2)
        getResponse(response.headers["Operation-Location"],key)
        # output = compilejs(textcode)
        return jsonify({'status':'ok'})
    return jsonify({'status':'file not found!!'})




def sendRequest(path):

    requestUrl = "https://centralindia.api.cognitive.microsoft.com/vision/v3.0/read/analyze?language=en"

    headers = {
    "Content-Type" : "application/octet-stream",
    "Ocp-Apim-Subscription-Key" : key,
    }

    params = {
    "language" : "en"
    }

    # this was a file which was on my local machine so change it accordingly
    body = open(path ,"rb").read()

    response = requests.request("POST",requestUrl,params = params,headers = headers, data = body)
    print(response.headers)

    return response

def getResponse(responseUrl:str,key:str):

    headers = {
        "Ocp-Apim-Subscription-Key" : key,
    }

    response = requests.request("GET",responseUrl,headers = headers)

    data2 = response.content.decode()
    for line in data2.analyzeResult.readResults[0].lines:
        print(line.text)



def compilejs(textcode):
    with open('submission.js','w+') as mycode:
        mycode.write(textcode)
    ccompile = Popen(["node","submission.js"], stderr=PIPE)
    ccompileerr = ccompile.communicate()[1].decode()
    if ccompileerr != '':
        return ccompileerr
    runoutput = Popen(["node ./submission..jsc"], stdout=PIPE)
    output = runoutput.communicate()[0]
    call(["rm","submission.js", "submission.jsc"])
    return output.decode()


if __name__ == '__main__':
    app.run(debug=True)