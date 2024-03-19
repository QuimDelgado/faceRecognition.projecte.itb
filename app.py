"""
Utiliza flask para recibir la imágen creada en local

app.py
Quim Delgado
"""

from flask import Flask, request, jsonify
import os

UPLOAD_FOLDER = 'C:/Users/quimd/Escritorio/face_rec/rebedor'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Comprueba si la petición tiene el archivo parte
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # Si el usuario no selecciona archivo, el navegador también
    # envía una parte vacía sin nombre de archivo
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
