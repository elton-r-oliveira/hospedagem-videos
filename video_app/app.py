from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.abspath('videos')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    videos = os.listdir(UPLOAD_FOLDER)
    print("Videos:", videos)
    print("UPLOAD_FOLDER:", os.path.abspath(UPLOAD_FOLDER))
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('index'))  # Fix: Add the function name
    return render_template('upload.html')

@app.route('/video/<path:filename>')
def video(filename):
    filename = filename.strip().lower()
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(video_path):
        return "Video not found.", 404
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True, mimetype='video/mp4')

@app.route('/watch/<path:filename>')
def watch(filename):
    filename = filename.strip().lower()
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(video_path):
        return "Video not found.", 404
    return render_template('watch.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)