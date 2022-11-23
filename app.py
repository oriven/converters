import flask
from flask import Flask, flash, redirect, render_template, request, Response,\
    url_for, send_file
from werkzeug.utils import secure_filename
from forms import SelectForm
from flask_basic_roles import BasicRoleAuth
import json
import os
import uuid

auth = BasicRoleAuth()
# auth.add_user(user='user', password='user123', roles='user')
auth.add_user(user='oriven', password='a123s123d123', roles='admin')


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = flask.Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

@app.route('/', methods=['GET'])
def main_page():
    return _show_page()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # file = request.files.getlist['file[]']
        app.logger.info(request.files)
        upload_files = request.files.getlist('file')
        app.logger.info(upload_files)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if not upload_files:
            flash('No selected file')
            return redirect(request.url)
        for file in upload_files:
            original_filename = file.filename
            extension = original_filename.rsplit('.', 1)[1].lower()
            filename = str(uuid.uuid1()) + '.' + extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
            files = _get_files()
            files[filename] = original_filename
            with open(file_list, 'w') as fh:
                json.dump(files, fh)
        flash('Upload succeded')
        return redirect(url_for('upload_file'))

@app.route('/download/<code>', methods=['GET'])
def download(code):
    files = _get_files()
    if code in files:
        path = os.path.join(UPLOAD_FOLDER, code)
        if os.path.exists(path):
            return send_file(path)
    abort(404)

def _show_page():
    files = _get_files()
    return render_template('upload.html', files=files)

def _get_files():
    file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
    if os.path.exists(file_list):
        with open(file_list) as fh:
            return json.load(fh)
    return {}
