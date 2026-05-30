"""
Reports and Analytics Module
ArewaSchool Manager v4
"""

import logging
from decimal import Decimal
from datetime import datetime
from pathlib import Path
from core.database import Database
from core.config import EXPORTS_DIR

logger = logging.getLogger(__name__)

class ReportsGenerator:
    """Generate various reports and analytics"""
    
    def __init__(self):
        self.db = Database()
        self.exports_dir = EXPORTS_DIR / "reports"
        self.exports_dir.mkdir(exist_ok=True)
    
    def generate_fees_report(self, academic_year):
        """Generate fees collection report"""
        try:
            summary = self.db.fetch_one('''
                SELECT
                    COUNT(*) as total_students,
                    SUM(total_amount) as total_fees,
                    SUM(amount_paid) as collected,
                    SUM(balance) as outstanding
                FROM fees
                WHERE academic_year = ?
            ''', (academic_year,))
            
            by_term = self.db.fetch_all('''
                SELECT term, COUNT(*) as count,
                       SUM(total_amount) as total,
                       SUM(amount_paid) as collected,
                       SUM(balance) as outstanding
                FROM fees
                WHERE academic_year = ?
                GROUP BY term
            ''', (academic_year,))
            
            return {
                "success": True,
                "summary": summary,
                "by_term": by_term
            }
        except Exception as e:
            logger.error(f"Error generating fees report: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_student_report(self, class_name=None):
        """Generate student enrollment report"""
        try:
            if class_name:
                students = self.db.fetch_all(
                    "SELECT class, COUNT(*) as count FROM students WHERE class = ? AND status = 'Active' GROUP BY class",
                    (class_name,)
                )
            else:
                students = self.db.fetch_all(
                    "SELECT class, COUNT(*) as count FROM students WHERE status = 'Active' GROUP BY class"
                )
            
            total = self.db.fetch_one(
                "SELECT COUNT(*) as total FROM students WHERE status = 'Active'"
            )
            
            return {
                "success": True,
                "by_class": students,
                "total": total['total']
            }
        except Exception as e:
            logger.error(f"Error generating student report: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_attendance_report(self, term, academic_year):
        """Generate attendance report"""
        try:
            attendance_data = self.db.fetch_all('''
                SELECT
                    s.full_name, s.reg_number, s.class,
                    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present,
                    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent,
                    COUNT(*) as total
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id AND a.term = ?
                WHERE s.status = 'Active'
                GROUP BY s.id
            ''', (term,))
            
            return {"success": True, "data": attendance_data}
        except Exception as e:
            logger.error(f"Error generating attendance report: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_performance_report(self, academic_year, term):
        """Generate student performance report"""
        try:
            performance = self.db.fetch_all('''
                SELECT
                    s.full_name, s.reg_number, s.class,
                    AVG(r.score) as average_score,
                    MAX(r.score) as highest_score,
                    MIN(r.score) as lowest_score,
                    COUNT(r.id) as subjects_taken
                FROM students s
                LEFT JOIN results r ON s.id = r.student_id AND r.academic_year = ? AND r.term = ?
                WHERE s.status = 'Active'
                GROUP BY s.id
                ORDER BY average_score DESC
            ''', (academic_year, term))
            
            return {"success": True, "data": performance}
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {"success": False, "error": str(e)}
    
    def get_dashboard_statistics(self):
        """Get dashboard statistics"""
        try:
            total_students = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM students WHERE status = 'Active'"
            )
            
            total_staff = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM staff WHERE status = 'Active'"
            )
            
            fees_collected = self.db.fetch_one(
                "SELECT SUM(amount_paid) as total FROM fees"
            )
            
            outstanding = self.db.fetch_one(
                "SELECT SUM(balance) as total FROM fees WHERE balance > 0"
            )
            
            return {
                "success": True,
                "total_students": total_students['count'],
                "total_staff": total_staff['count'],
                "fees_collected": float(fees_collected['total'] or 0),
                "outstanding_fees": float(outstanding['total'] or 0)
            }
        except Exception as e:
            logger.error(f"Error getting dashboard statistics: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    generator = ReportsGenerator()
    print("ReportsGenerator initialized")