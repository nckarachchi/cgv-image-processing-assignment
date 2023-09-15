import datetime
from PIL import Image
import numpy as np
import pytesseract
import xml.etree.ElementTree as ET
import pymongo

# pytesseract windows file location of external added
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = 'C:\\Users\\admmin\\Documents\\cgv\\cgv-coursework-image-proccesing\\attendance-management-backend\\src\\assets\\attendance_sheet2.png'
image = Image.open(image_path)

gray_image = image.convert('L')

threshold = 200
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

#genarate xml
tree = ET.ElementTree(root)
tree.write("info.xml")

print("Attendance information extracted and saved as info.xml")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["attendance_database"]
collection = db["attendance_collection"]

current_date = datetime.now()

for line in lines:
    parts = line.strip().split()
    if len(parts) >= 3:
        index, name, signature = parts[0], ' '.join(parts[1:-1]), parts[-1]
        present = 'Present' if signature else 'Absent'

        student_doc = {
            "Index": index,
            "Name": name,
            "Status": present,
            "Date": current_date
        }

        collection.insert_one(student_doc)

print("Attendance information extracted and saved in the MongoDB database.")

client.close()
