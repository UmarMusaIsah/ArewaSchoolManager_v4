"""
Attendance Management Module
ArewaSchool Manager v4
"""

import logging
from datetime import datetime
from core.database import Database
from core.config import ATTENDANCE_STATUS

logger = logging.getLogger(__name__)

class AttendanceManager:
    """Handle attendance tracking"""
    
    def __init__(self):
        self.db = Database()
    
    def mark_attendance(self, data):
        """Mark attendance for a student"""
        try:
            if data['status'] not in ATTENDANCE_STATUS:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(ATTENDANCE_STATUS)}")
            
            self.db.execute('''
                INSERT INTO attendance (
                    student_id, date, status, class, term, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['student_id'], data.get('date', datetime.now().date()),
                data['status'], data.get('class'),
                data.get('term'), data.get('recorded_by')
            ))
            
            logger.info(f"Attendance marked for student {data['student_id']}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error marking attendance: {e}")
            return {"success": False, "error": str(e)}
    
    def get_attendance(self, student_id, date=None):
        """Get attendance records for a student"""
        try:
            if date:
                records = self.db.fetch_all(
                    "SELECT * FROM attendance WHERE student_id = ? AND date = ?",
                    (student_id, date)
                )
            else:
                records = self.db.fetch_all(
                    "SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC",
                    (student_id,)
                )
            
            return {"success": True, "data": records}
        except Exception as e:
            logger.error(f"Error fetching attendance: {e}")
            return {"success": False, "error": str(e)}
    
    def get_class_attendance(self, class_name, date):
        """Get attendance for entire class"""
        try:
            records = self.db.fetch_all(
                "SELECT * FROM attendance WHERE class = ? AND date = ?",
                (class_name, date)
            )
            return {"success": True, "data": records}
        except Exception as e:
            logger.error(f"Error fetching class attendance: {e}")
            return {"success": False, "error": str(e)}
    
    def get_attendance_statistics(self, student_id, term):
        """Get attendance statistics"""
        try:
            total = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND term = ?",
                (student_id, term)
            )
            
            present = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND term = ? AND status = 'Present'",
                (student_id, term)
            )
            
            absent = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND term = ? AND status = 'Absent'",
                (student_id, term)
            )
            
            return {
                "success": True,
                "total": total['count'],
                "present": present['count'],
                "absent": absent['count'],
                "percentage": (present['count'] / total['count'] * 100) if total['count'] > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error calculating attendance statistics: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    manager = AttendanceManager()
    print("AttendanceManager initialized")