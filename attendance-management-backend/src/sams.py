import datetime
from PIL import Image
import numpy as np
import pytesseract
import xml.etree.ElementTree as ET
import pymongo

# Path to your Tesseract OCR executable (modify as needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image_path = 'C:\\Users\\admmin\\Documents\\cgv\\cgv-coursework-image-proccesing\\attendance-management-backend\\src\\assets\\attendance_sheet2.png'
image = Image.open(image_path)

# Convert the image to grayscale
gray_image = image.convert('L')

# Binarize the image using a threshold
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
tree.write("info.xml")

print("Attendance information extracted and saved as info.xml")
# Initialize a MongoDB client and connect to a local MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["attendance_database"]
collection = db["attendance_collection"]

# Get the current date
current_date = datetime.now()

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

print("Attendance information extracted and saved in the MongoDB database.")

# Close the MongoDB client connection when done
client.close()