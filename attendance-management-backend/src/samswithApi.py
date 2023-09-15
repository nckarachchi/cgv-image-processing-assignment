import datetime
import pytesseract
import xml.etree.ElementTree as ET
import pymongo
from flask import Flask, request, jsonify, send_file
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# api call which is connected with frontend react
@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

# image open 
    image = Image.open(image_file)
# genarate gray image
    gray_image = image.convert('L')
    threshold = 200
# genarate binary image
    binary_image = gray_image.point(lambda p: p > threshold and 255)

    text = pytesseract.image_to_string(binary_image)

    lines = text.split('\n')

    root = ET.Element("Attendance")

    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            index, name, signature = parts[0], ' '.join(parts[1:-1]), parts[-1]
            present = 'Present' if signature else 'Absent'

            student = ET.SubElement(root, "Student")
            ET.SubElement(student, "Index").text = index
            ET.SubElement(student, "Name").text = name
            ET.SubElement(student, "Status").text = present

    tree = ET.ElementTree(root)
    tree_str = ET.tostring(root, encoding='utf-8')
    xml_file = io.BytesIO(tree_str)
    xml_file.seek(0)

# connection of mongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["attendance_database"]
    collection = db["attendance_collection"]

    current_date = datetime.datetime.now()
# check present of the student
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            index, name, signature = parts[0], ' '.join(parts[1:-1]), parts[-1]
            present = 'Present' if signature else 'Absent'
# mongo Db document add
            student_doc = {
                "Index": index,
                "Name": name,
                "Status": present,
                "Date": current_date
            }

            collection.insert_one(student_doc)

    client.close()

    return send_file(xml_file, as_attachment=True, download_name="info.xml")

if __name__ == '__main__':
    app.run(debug=True)  
