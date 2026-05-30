"""
Staff Management Module
ArewaSchool Manager v4
"""

import logging
from core.database import Database
from core.utils import Utils

logger = logging.getLogger(__name__)

class StaffManager:
    """Handle all staff-related operations"""
    
    def __init__(self):
        self.db = Database()
    
    def add_staff(self, data):
        """Add new staff member"""
        try:
            staff_id = Utils.generate_staff_id()
            
            self.db.execute('''
                INSERT INTO staff (
                    staff_id, full_name, role, department,
                    phone, email, salary, hire_date, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                staff_id, data['full_name'], data['role'],
                data.get('department'), data.get('phone'),
                data.get('email'), data.get('salary'),
                data.get('hire_date'), 'Active'
            ))
            
            logger.info(f"Staff member {data['full_name']} added with ID: {staff_id}")
            return {"success": True, "staff_id": staff_id}
        except Exception as e:
            logger.error(f"Error adding staff: {e}")
            return {"success": False, "error": str(e)}
    
    def get_staff(self):
        """Get all staff members"""
        try:
            staff = self.db.fetch_all(
                "SELECT * FROM staff WHERE status = 'Active' ORDER BY full_name"
            )
            return {"success": True, "data": staff}
        except Exception as e:
            logger.error(f"Error fetching staff: {e}")
            return {"success": False, "error": str(e)}
    
    def get_staff_by_role(self, role):
        """Get staff by role"""
        try:
            staff = self.db.fetch_all(
                "SELECT * FROM staff WHERE role = ? AND status = 'Active'",
                (role,)
            )
            return {"success": True, "data": staff}
        except Exception as e:
            logger.error(f"Error fetching staff: {e}")
            return {"success": False, "error": str(e)}
    
    def update_staff(self, staff_id, data):
        """Update staff information"""
        try:
            self.db.execute('''
                UPDATE staff SET
                full_name = ?, role = ?, department = ?,
                phone = ?, email = ?, salary = ?,
                updated_at = CURRENT_TIMESTAMP
                WHERE staff_id = ?
            ''', (
                data['full_name'], data['role'],
                data.get('department'), data.get('phone'),
                data.get('email'), data.get('salary'),
                staff_id
            ))
            
            logger.info(f"Staff member {staff_id} updated")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating staff: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_staff(self, staff_id):
        """Soft delete staff (mark as inactive)"""
        try:
            self.db.execute(
                "UPDATE staff SET status = 'Inactive' WHERE staff_id = ?",
                (staff_id,)
            )
            
            logger.info(f"Staff member {staff_id} deleted (marked inactive)")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting staff: {e}")
            return {"success": False, "error": str(e)}
    
    def get_staff_count(self):
        """Get total active staff"""
        try:
            result = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM staff WHERE status = 'Active'"
            )
            return {"success": True, "count": result['count']}
        except Exception as e:
            logger.error(f"Error getting staff count: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    manager = StaffManager()
    print("StaffManager initialized")