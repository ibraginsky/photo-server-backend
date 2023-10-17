from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
# from PIL import Image

app = Flask(__name__)


# Путь к папке с изображениями
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


# Функция для проверки разрешения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Получение списка файлов в папке
    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    # return render_template('index.html', image_files=image_files)
    return image_files


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        # Загрузка файла
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File uploaded successfully"
    return "Invalid file format"


@app.route('/image/<filename>')
def get_image(filename):
    # Отправка изображения
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run()
