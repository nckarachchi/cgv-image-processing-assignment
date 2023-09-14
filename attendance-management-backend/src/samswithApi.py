import datetime
import pytesseract
import xml.etree.ElementTree as ET
import pymongo
from flask import Flask, request, jsonify, send_file
from PIL import Image
import io

# Path to your Tesseract OCR executable (modify as needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    # Check if an image was included in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    # Process the image as you did before
    image = Image.open(image_file)
    gray_image = image.convert('L')
    threshold = 200
    binary_image = gray_image.point(lambda p: p > threshold and 255)

    # Perform OCR (Optical Character Recognition) to extract text from the image
    text = pytesseract.image_to_string(binary_image)

    # Split the extracted text into lines
    lines = text.split('\n')

    # Create an XML tree to store attendance information
    root = ET.Element("Attendance")

    # Process each line to extract index, name, and attendance status
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            index, name, signature = parts[0], ' '.join(parts[1:-1]), parts[-1]
            present = 'Present' if signature else 'Absent'

            # Create XML elements for each student
            student = ET.SubElement(root, "Student")
            ET.SubElement(student, "Index").text = index
            ET.SubElement(student, "Name").text = name
            ET.SubElement(student, "Status").text = present

    # Create an XML file to store the attendance information
    tree = ET.ElementTree(root)
    tree_str = ET.tostring(root, encoding='utf-8')
    xml_file = io.BytesIO(tree_str)
    xml_file.seek(0)

    # Initialize a MongoDB client and connect to a local MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["attendance_database"]
    collection = db["attendance_collection"]

    # Get the current date
    current_date = datetime.datetime.now()

    # Process each line to extract index, name, and attendance status
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            index, name, signature = parts[0], ' '.join(parts[1:-1]), parts[-1]
            present = 'Present' if signature else 'Absent'

            # Create a document to insert into MongoDB with the current date
            student_doc = {
                "Index": index,
                "Name": name,
                "Status": present,
                "Date": current_date
            }

            # Insert the document into the MongoDB collection
            collection.insert_one(student_doc)

    # Close the MongoDB client connection when done
    client.close()

    return send_file(xml_file, as_attachment=True, download_name="info.xml")

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
