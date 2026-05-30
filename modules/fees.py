"""
Fees Management Module
ArewaSchool Manager v4
"""

import logging
from decimal import Decimal
from core.database import Database
from core.utils import Utils, validate_fee_data, ValidationError

logger = logging.getLogger(__name__)

class FeesManager:
    """Handle all fee-related operations"""
    
    def __init__(self):
        self.db = Database()
    
    def record_payment(self, data):
        """Record fee payment"""
        try:
            validate_fee_data(data)
            
            fees = self.db.fetch_one(
                "SELECT * FROM fees WHERE student_id = ? AND term = ? AND academic_year = ?",
                (data['student_id'], data['term'], data['academic_year'])
            )
            
            if not fees:
                total = Decimal(str(data['total_amount']))
                receipt_number = Utils.generate_receipt_number()
                
                self.db.execute('''
                    INSERT INTO fees (
                        student_id, term, academic_year,
                        total_amount, amount_paid, balance,
                        payment_method, receipt_number, recorded_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['student_id'], data['term'], data['academic_year'],
                    total, total, 0,
                    data.get('payment_method'), receipt_number,
                    data.get('recorded_by')
                ))
                
                logger.info(f"Fee payment recorded for student {data['student_id']}")
                return {"success": True, "receipt_number": receipt_number}
            else:
                amount_paid = Decimal(str(fees['amount_paid'])) + Decimal(str(data['total_amount']))
                balance = Decimal(str(fees['total_amount'])) - amount_paid
                
                self.db.execute('''
                    UPDATE fees SET
                    amount_paid = ?, balance = ?,
                    payment_date = ?, payment_method = ?,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE student_id = ? AND term = ? AND academic_year = ?
                ''', (
                    amount_paid, max(balance, 0),
                    data.get('payment_date'), data.get('payment_method'),
                    data['student_id'], data['term'], data['academic_year']
                ))
                
                return {"success": True, "balance": balance}
        
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Error recording payment: {e}")
            return {"success": False, "error": str(e)}
    
    def get_fees(self, student_id):
        """Get all fees for a student"""
        try:
            fees = self.db.fetch_all(
                "SELECT * FROM fees WHERE student_id = ? ORDER BY academic_year DESC, term DESC",
                (student_id,)
            )
            return {"success": True, "data": fees}
        except Exception as e:
            logger.error(f"Error fetching fees: {e}")
            return {"success": False, "error": str(e)}
    
    def get_outstanding_fees(self):
        """Get all outstanding fees"""
        try:
            outstanding = self.db.fetch_all(
                "SELECT * FROM fees WHERE balance > 0 ORDER BY academic_year DESC"
            )
            return {"success": True, "data": outstanding}
        except Exception as e:
            logger.error(f"Error fetching outstanding fees: {e}")
            return {"success": False, "error": str(e)}
    
    def get_total_collected(self, academic_year=None):
        """Get total fees collected"""
        try:
            if academic_year:
                result = self.db.fetch_one(
                    "SELECT SUM(amount_paid) as total FROM fees WHERE academic_year = ?",
                    (academic_year,)
                )
            else:
                result = self.db.fetch_one(
                    "SELECT SUM(amount_paid) as total FROM fees"
                )
            
            total = Decimal(str(result['total'] or 0))
            return {"success": True, "total": float(total)}
        except Exception as e:
            logger.error(f"Error calculating total: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    manager = FeesManager()
    print("FeesManager initialized")