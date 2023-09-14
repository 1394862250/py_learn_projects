import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from PIL import Image
from flask import send_file

model = keras.models.load_model('D:/2023/cvsx/model/hand_gesture_model.h5')

def predict_image(image_path):
    img = keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img = img.resize((64, 64), resample=Image.BILINEAR)
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create batch axis
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['01_palm', '02_l','03_fist','04_fist_moved','05_thumb','06_index','07_ok','08_palm_moved','09_c','10_down']
    predicted_class = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)
    return predicted_class, confidence

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/img/<path:filename>')
def get_image(filename):
    return send_file(f'templates/img/{filename}', mimetype='image/png')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        predicted_class, confidence = predict_image(file_path)
        result_text = '类为: {} ({:.2f}% 可能性)'.format(predicted_class, confidence)
        return render_template('result.html', result_text=result_text, image_file=filename)
    else:
        return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
