import sqlite3
from PIL import Image
import io


db_path = r'C:\Users\arpan\OneDrive\Desktop\FolderCreate\TreeCameraWebsite\myProject\Treecollection.db'


conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("SELECT image_blob, prediction, confidence, timestamp FROM predictions ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

if row:
    img_data, prediction, confidence, timestamp = row
    image = Image.open(io.BytesIO(img_data))
    image.show()

    print(f"Prediction: {prediction}")
    print(f"Confidence: {confidence}")
    print(f"Timestamp: {timestamp}")
else:
    print("No image found in the database.")

conn.close()
