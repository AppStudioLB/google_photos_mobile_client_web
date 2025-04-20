import os
import concurrent.futures
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from gpmc import Client  # google_photos_mobile_client
import sys
import io
import threading
import contextlib
import webbrowser

app = Flask(__name__)
app.secret_key = "Secret_Key" 
app.config['UPLOAD_FOLDER'] = 'uploads'   
app.config['MAX_CONTENT_LENGTH'] = 100000 * 1024 * 1024  


AUTH_DATA = "ENTER_YOURS"


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def upload_file():

    client = Client(auth_data=AUTH_DATA)
    result = client.upload(target=app.config['UPLOAD_FOLDER'], show_progress=True, threads=5, delete_from_host=True)
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('업로드할 파일이 없습니다.')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        if not files or all(file.filename == "" for file in files):
            flash('선택된 파일이 없습니다.')
            return redirect(request.url)
        
    
        for file in files:
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
        
        try:
            result = upload_file()
            flash("업로드가 성공적으로 완료되었습니다!")
        except Exception as e:
            flash(f"업로드 실패: {e}")
        
        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
 
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}"


    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
         webbrowser.open_new_tab(url)

    app.run(host=host, port=port, debug=True, threaded=True)