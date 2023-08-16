import os, json, time, csv
from flask import *
from werkzeug.utils import secure_filename
# from models.a0cy_model import A0CYModel
# from models.lloan_model import LLOANModel
from ftplib import FTP
import requests

# File requirement
UPLOAD_FOLDER = 'file_uploads'
ALLOWED_EXTENSIONS = {'txt'}

# FTP Host
FTP_HOST = "179.61.188.27"
FTP_USER = "arsyad"
FTP_PASSWORD = "Petromax123."
FTP_FILES_DIR = "/ftp/upload"

# DWH Host
DWH_HOST = "https://develop.bankumkm.id/datawarehouse"
DWH_TOKEN = "$2y$10$uK7wv2xbmgOFAWOA./7nn.RMkuDfg4FKy64ad4h0AVqKxEpt0Co2u"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FTP_HOST'] = FTP_HOST
app.config['FTP_USER'] = FTP_USER
app.config['FTP_PASSWORD'] = FTP_PASSWORD
app.config['FTP_FILES_DIR'] = FTP_FILES_DIR
app.config['DWH_HOST'] = DWH_HOST
app.config['DWH_TOKEN'] = DWH_TOKEN


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(path):
    with open(path, 'r') as in_file:
        return in_file.readlines()

def split_data_with_dictionary(data, dictionary):
    # Split data
    result = []
    for i in range(len(data)):
        val = data[i].strip()
        objects = {}
        for j in dictionary:
            value = val[(j['from']-1):j['to']]
            value = value.lstrip().rstrip()
            objects[j['field']] = value
        result.append(objects)
    return result

def get_dictionary(filename):
    url = "".join([app.config['DWH_HOST'],"/api/v1/dictionary"])
    params = {'filename': filename}
    headers =  {"mid-client-key": app.config['DWH_TOKEN']}

    response = requests.get(url,params=params, headers=headers)
    
    return response.json()

@app.route('/', methods=['POST'])
def post_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        response = {
            'status': 'failed',
            'message': 'No file choosen.'
        }
        return jsonify(response), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename
    if file.filename == '':
        response = {
            'status': 'failed',
            'message': 'No file choosen.'
        }
        return jsonify(response), 400
    if file and allowed_file(file.filename):
        # Get uploaded file
        filename = secure_filename(file.filename)
        filename_split = filename.split('.')[0]
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        res = get_dictionary(filename_split)
        items = res['data']['item']
        # for i in range(len(items)):
        for x in items:
            print(x['field'])

        text = read_file(path=path)
        text.remove("")
        result = text
        final_result = split_data_with_dictionary(result, items)

        # Connect ftp
        # ftp = connect_ftp()

        response = {
            'status': 'success',
            'message': 'Successfully upload file.',
            'file': text,
            'data': final_result,
        }
        return jsonify(response), 200

@app.route('/tes', methods=['GET'])
def tes():
    res = get_dictionary("A0CY")

    return jsonify(res), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)