import os, json, time, csv
from flask import *
from werkzeug.utils import secure_filename
import models.a0cy_model as my_model
import models.lloan_model as loan_model
from ftplib import FTP

# File requirement
UPLOAD_FOLDER = 'file_uploads'
ALLOWED_EXTENSIONS = {'txt'}

# FTP Host
FTP_HOST = "179.61.188.27"
FTP_USER = "arsyad"
FTP_PASSWORD = "Petromax123."
FTP_FILES_DIR = "/ftp/upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FTP_HOST'] = FTP_HOST
app.config['FTP_USER'] = FTP_USER
app.config['FTP_PASSWORD'] = FTP_PASSWORD
app.config['FTP_FILES_DIR'] = FTP_FILES_DIR

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(path):
    with open(path, 'r') as in_file:
        return in_file.readlines()
    
def connect_ftp():
    ftp = FTP(app.config['FTP_HOST'], app.config['FTP_USER'], app.config['FTP_PASSWORD'])
    filename = 'A0CY.txt'
    dir = app.config['FTP_FILES_DIR']
    # change directory
    ftp.cwd(dir)
    # show current directory
    ftp.dir()
    # show current directory files
    ftp.retrlines('LIST')
    with open(filename, 'r') as file:
        # Command for Downloading the file "RETR filename"
        ftp.retrbinary(f"RETR {dir,'/',filename}", file.write)
        ftp.ret
        print('--------File values--------')
        print(file.readlines())
        print('--------End file values--------')
    return file
    
def split_data(data):
    # Set dictionary
    dict1 = my_model.A0CYModel("CYSTAT", 1, 1, 1, "Status Record")
    dict2 = my_model.A0CYModel("CYCODE", 2, 4, 3, "Currency Code")
    dict3 = my_model.A0CYModel("CYNAME", 5, 34, 30, "Currency Name")
    dict4 = my_model.A0CYModel("CYDTLC", 35, 42, 8, "Tanggal Diubah")
    dict5 = my_model.A0CYModel("CYDECI", 43, 43, 1, "Decimal Point")
    arr_code = ['CYSTAT', 'CYCODE', 'CYNAME', 'CYDTLC', 'CYDECI']
    arr_desc = ['Status Record', 'Currency Code', 'Currency Name', 'Tanggal Diubah', 'Decimal Point']

    # Convert object to json serialized
    # json_str1 = json.dumps(dict1.__dict__)
    # json_str2 = json.dumps(dict2.__dict__)
    # json_str3 = json.dumps(dict3.__dict__)
    # json_str4 = json.dumps(dict4.__dict__)
    # json_str5 = json.dumps(dict5.__dict__)

    all_dict = []
    all_dict.append(dict1)
    all_dict.append(dict2)
    all_dict.append(dict3)
    all_dict.append(dict4)
    all_dict.append(dict5)
    
    # Split data
    result = []
    for i in range(len(data)):
        val = data[i].strip()
        objects = {}
        for j in range(len(arr_code)):
            value = val[(all_dict[j].froms - 1):all_dict[j].to]
            value = value.lstrip().rstrip()
            objects[arr_code[j]] = value
        result.append(objects)
    return result

def split_data_lloan(data):
    # Set dictionary
    dict1 = loan_model.LLOANModel("L0STAT", 1, 1, 1, "Status Record")
    dict2 = loan_model.LLOANModel("L0STAD", 2, 2, 1, "Status Data")
    dict3 = loan_model.LLOANModel("L0BRCA", 3, 4, 2, "Wilayah")
    dict4 = loan_model.LLOANModel("L0BRCD", 5, 7, 3, "Branch")
    dict5 = loan_model.LLOANModel("L0CSNO", 8, 15, 8, "Customer code")
    arr_code = ['L0STAT', 'L0STAD', 'L0BRCA', 'L0BRCD', 'L0CSNO']
    arr_desc = ['Status Record', 'Status Data', 'Wilayah', 'Branch', 'Customer code']

    # Convert object to json serialized
    # json_str1 = json.dumps(dict1.__dict__)
    # json_str2 = json.dumps(dict2.__dict__)
    # json_str3 = json.dumps(dict3.__dict__)
    # json_str4 = json.dumps(dict4.__dict__)
    # json_str5 = json.dumps(dict5.__dict__)

    all_dict = []
    all_dict.append(dict1)
    all_dict.append(dict2)
    all_dict.append(dict3)
    all_dict.append(dict4)
    all_dict.append(dict5)
    
    # Split data
    result = []
    for i in range(len(data)):
        val = data[i].strip()
        objects = {}
        for j in range(len(arr_code)):
            value = val[(all_dict[j].froms - 1):all_dict[j].to]
            value = value.lstrip().rstrip()
            objects[arr_code[j]] = value
        result.append(objects)
    return result

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
        # # Get uploaded file
        # filename = secure_filename(file.filename)
        # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(path)

        # text = read_file(path=path)
        # text.remove("")
        # result = text
        # final_result = split_data(result)
        ftp = connect_ftp()
        response = {
            'status': 'success',
            'message': 'Successfully upload file.',
            'data': ftp,
        }
        return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)