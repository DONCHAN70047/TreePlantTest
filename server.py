import sys
import base64
import io
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import traceback
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  


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


if prediction > 0.5:
    print(f"Not healthy.....{prediction}")
else:
    print(f"Healthy....{prediction}")
