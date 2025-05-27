import sys
import base64
import io
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import os
import sqlite3
from datetime import datetime


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    model = tf.keras.models.load_model("public/Model2.keras")

    input_data = sys.stdin.read()

    if ',' in input_data:
        input_data = input_data.split(',')[1]


    img_bytes = base64.b64decode(input_data)
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    target_size = model.input_shape[1:3]
    img = img.resize(target_size)
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    val = model.predict(x, verbose=0)
    prediction = float(val[0][0])

    result_text = "Healthy" if prediction <= 0.5 else "Not healthy"
    print(f"{result_text}....{prediction}")

    db_path = 'Treecollection.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_blob BLOB,
            prediction TEXT,
            confidence FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    cursor.execute(
        "INSERT INTO predictions (image_blob, prediction, confidence) VALUES (?, ?, ?)",
        (img_bytes, result_text, prediction)
    )

    conn.commit()
    conn.close()

except Exception as e:
    print("Error:", str(e))
    sys.exit(1)
