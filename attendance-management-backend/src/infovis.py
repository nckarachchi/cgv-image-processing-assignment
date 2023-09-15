import pymongo

class InfoVis:
    def __init__(self):
        # Initialize a MongoDB client and connect to a local MongoDB server
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["attendance_database"]
        self.collection = self.db["attendance_collection"]

    def get_attendance_summary(self, student_index):

        cursor = self.collection.find({"Index": student_index})
        
        # Initialize attendance count variables
        present_count = 0
        absent_count = 0
        
        for document in cursor:
            status = document["Status"]
            if status == "Present":
                present_count += 1
            elif status == "Absent":
                absent_count += 1
        
        # Create a dictionary
        summary = {
            "student_index": student_index,
            "present_count": present_count,
            "absent_count": absent_count
        }
        
        return summary

    def close_connection(self):
        # Close part
        self.client.close()
