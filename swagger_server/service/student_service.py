import os
from pymongo import MongoClient

# 🔹 MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["student_db"]  # Database Name
student_collection = db["students"]  # Collection Name


def add(student=None):
    """Adds a student to MongoDB, ensuring uniqueness based on first and last name."""
    if not student:
        return "Invalid student data", 400

    # Check if a student with this student id already exists
    existing_student = student_collection.find_one({
        "student_id": student.student_id
    })

    if existing_student:
        return "already exists", 409

    # Insert new student
    student_dict = student.to_dict()
    return student_collection.insert_one(student_dict)


def get_by_id(student_id=None, subject=None):
    """Retrieves a student by ID from MongoDB."""
    if not student_id:
        return "Student ID is required", 400

    student = student_collection.find_one({"student_id": student_id})

    if not student:
        return "not found", 404

    return student

def delete(student_id=None):
    """Deletes a student from MongoDB by ID."""
    if not student_id:
        return "Student ID is required", 400

    result = student_collection.delete_one({"student_id": student_id})

    if result.deleted_count == 0:
        return "not found", 404

    return student_id
