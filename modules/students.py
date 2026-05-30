"""
Student Management Module
ArewaSchool Manager v4
"""

import logging
from core.database import Database
from core.utils import Utils, validate_student_data, ValidationError

logger = logging.getLogger(__name__)

class StudentManager:
    """Handle all student-related operations"""
    
    def __init__(self):
        self.db = Database()
    
    def add_student(self, data):
        """Add new student"""
        try:
            validate_student_data(data)
            
            cursor = self.db.fetch_all("SELECT COUNT(*) FROM students")
            student_id = cursor[0][0] + 1 if cursor else 1
            
            reg_number = Utils.generate_reg_number(data['class'], student_id)
            
            self.db.execute('''
                INSERT INTO students (
                    reg_number, full_name, class, gender,
                    date_of_birth, parent_name, parent_phone,
                    parent_email, address, enrollment_date, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reg_number, data['full_name'], data['class'],
                data.get('gender'), data.get('date_of_birth'),
                data['parent_name'], data['parent_phone'],
                data.get('parent_email'), data.get('address'),
                data.get('enrollment_date'), 'Active'
            ))
            
            logger.info(f"Student {data['full_name']} added with reg#: {reg_number}")
            return {"success": True, "reg_number": reg_number}
        
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Error adding student: {e}")
            return {"success": False, "error": str(e)}
    
    def get_students(self, class_name=None):
        """Get all students or filter by class"""
        try:
            if class_name:
                students = self.db.fetch_all(
                    "SELECT * FROM students WHERE class = ? AND status = 'Active'",
                    (class_name,)
                )
            else:
                students = self.db.fetch_all(
                    "SELECT * FROM students WHERE status = 'Active'"
                )
            
            return {"success": True, "data": students}
        except Exception as e:
            logger.error(f"Error fetching students: {e}")
            return {"success": False, "error": str(e)}
    
    def get_student(self, student_id):
        """Get single student by ID"""
        try:
            student = self.db.fetch_one(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )
            
            return {"success": True, "data": student}
        except Exception as e:
            logger.error(f"Error fetching student: {e}")
            return {"success": False, "error": str(e)}
    
    def update_student(self, student_id, data):
        """Update student information"""
        try:
            self.db.execute('''
                UPDATE students SET
                full_name = ?, class = ?, gender = ?,
                date_of_birth = ?, parent_name = ?,
                parent_phone = ?, parent_email = ?,
                address = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                data['full_name'], data['class'],
                data.get('gender'), data.get('date_of_birth'),
                data['parent_name'], data['parent_phone'],
                data.get('parent_email'), data.get('address'),
                student_id
            ))
            
            logger.info(f"Student {student_id} updated")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating student: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_student(self, student_id):
        """Soft delete student (mark as inactive)"""
        try:
            self.db.execute(
                "UPDATE students SET status = 'Inactive' WHERE id = ?",
                (student_id,)
            )
            
            logger.info(f"Student {student_id} deleted (marked inactive)")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting student: {e}")
            return {"success": False, "error": str(e)}
    
    def get_student_count(self):
        """Get total active students"""
        try:
            result = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM students WHERE status = 'Active'"
            )
            return {"success": True, "count": result['count']}
        except Exception as e:
            logger.error(f"Error getting student count: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    manager = StudentManager()
    print("StudentManager initialized")