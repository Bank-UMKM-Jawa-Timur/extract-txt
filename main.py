import os, time, sys
from flask import *
from werkzeug.utils import secure_filename
from ftplib import FTP
import requests
import json as my_json
import urllib.request
import urllib
from urllib.request import urlopen
import urllib3

# Host
HOST = '0.0.0.0'
PORT = 5001

# File requirement
UPLOAD_FOLDER = 'file_uploads'
ALLOWED_EXTENSIONS = {'txt'}

# FTP Host
FTP_HOST = "179.61.188.27"
FTP_USER = "arsyad"
FTP_PASSWORD = "Petromax123."
FTP_FILES_DIR = "/ftp/upload"

# DWH Host
# DWH_HOST = "https://develop.bankumkm.id/datawarehouse"
DWH_TOKEN = "$2y$10$uK7wv2xbmgOFAWOA./7nn.RMkuDfg4FKy64ad4h0AVqKxEpt0Co2u"
DWH_HOST = "http://127.0.0.1:8000"

app = Flask(__name__)
app.config['HOST'] = HOST
app.config['PORT'] = PORT
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

def read_file(url):
    print(f'read file from {url}')
    data = urllib.request.urlopen(url)
    result = my_json.load(data)
    # for line in data:
    #     result.append(line.decode("ISO-8859-1"))
    return result
    # with open(url, 'r',encoding="ISO-8859-1") as in_file:
    #     return in_file.readlines()

def split_data_with_dictionary(data, dictionary):
    # Split data
    print('split data')
    result = []
    for i in range(len(data)):
        val = data[i].strip()
        objects = {}
        for j in dictionary:
            value = val[(j['from']-1):j['to']]
            value = value.lstrip().rstrip()
            objects[j['field']] = value
        result.append(objects)
    print('split data done')
    
    return result

def save_json(data, filename, total_all_data, page):
    print("save response to json file")
    path = f"json/{filename}"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    #printing if the path exists or not
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")

    limit = 1000 # limit per page
    total_data = data['total']
    total_page = int(total_data / limit)

    # if (total_data > limit):
    #     start_index = 0
    #     end_index = limit
    #     for page in range(1, total_data):
    #         save_file = open(f"{path}/{filename}_{page}.json", "w")
    #         start_index = limit * page - limit
    #         if (page > 1):
    #             end_index = limit * page
    #         value = {
    #             'total': total_data,
    #             'total_per_page': len(data['data'][start_index:end_index]),
    #             'data': data['data'][start_index:end_index]
    #         }
    #         my_json.dump(value, save_file, indent = 6)
    #         save_file.close()
    # else:
    save_file = open(f"{path}/{filename}_{page}.json", "w")
    value = {
        'total': total_data,
        'total_all_data': total_all_data,
        'data': data['data']
    }
    my_json.dump(value, save_file, indent = 6)
    save_file.close()
    
    print("file saved")


@app.route('/extract', methods=['POST'])
def post_file():
    if request.method == 'POST':
        try:
            # Request body
            page = request.json['page']
            filename = request.json['file']
            total_all_data = request.json['total']
            items = request.json['dictionary']
            text = request.json['file_json']

            result = text
            final_result = split_data_with_dictionary(result, items)

            final_result = {
                'total_all_data': total_all_data,
                'total': len(final_result),
                'data': final_result
            }

            # Save json file
            save_json(final_result, filename, total_all_data, page)

            response = {
                'status': 'success',
                'message': 'Successfully upload file.',
                'filename': filename    
            }

            return jsonify(response), 200
        except Exception as e:
            print('error')
            print(e)
            response = {
                'status': 'failed',
                'message': 'Failed to upload file.',
                'detail': str(e)
            }

            return jsonify(response), 500

@app.route('/json', methods=['GET'])
def json():
    req = request.args
    page = int(req['page'])
    filepath = f"json/{req['filename']}/{req['filename']}_{page}.json"

    if (os.path.exists(filepath)):
        json_file = open(filepath, "r")
        json = my_json.load(json_file)
        json_file.close()
        status = 200
    else:
        json = {
            'status': 'failed',
            'message': 'File not found'
        }
        status = 404

    return json, status

if __name__ == "__main__":
    app.run(host=HOST, debug=True,port=PORT)