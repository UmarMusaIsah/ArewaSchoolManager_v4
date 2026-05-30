"""
Utility Functions
"""
import re
import logging
import hashlib
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class Utils:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        pattern = r'^[\d\s\-\+\(\)]{10,}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def generate_reg_number(class_name: str, student_id: int) -> str:
        year = datetime.now().year
        return f"{year}-{class_name.replace(' ', '')}-{student_id:04d}"
    
    @staticmethod
    def generate_receipt_number() -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"RCP-{timestamp}"
    
    @staticmethod
    def generate_staff_id() -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"STF-{timestamp}"
    
    @staticmethod
    def format_currency(amount: float) -> str:
        return f"₦{amount:,.2f}"
    
    @staticmethod
    def format_date(date_str: str, format_str: str = "%d-%m-%Y") -> str:
        try:
            date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
            return date_obj.strftime(format_str)
        except Exception as e:
            logger.error(f"Date formatting error: {e}")
            return str(date_str)
    
    @staticmethod
    def get_age(date_of_birth: str) -> int:
        try:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.today()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except Exception as e:
            logger.error(f"Age calculation error: {e}")
            return 0
    
    @staticmethod
    def calculate_grade(score: float) -> str:
        from core.config import GRADES
        for grade, (min_score, max_score) in GRADES.items():
            if min_score <= score <= max_score:
                return grade
        return "F"
    
    @staticmethod
    def truncate_text(text: str, length: int = 50) -> str:
        if len(text) > length:
            return text[:length] + "..."
        return text
    
    @staticmethod
    def get_current_academic_year() -> str:
        current_year = datetime.now().year
        return f"{current_year}/{current_year + 1}"
    
    @staticmethod
    def get_current_term() -> str:
        month = datetime.now().month
        if month in [1, 2, 3, 4]:
            return "First Term"
        elif month in [5, 6, 7, 8]:
            return "Second Term"
        else:
            return "Third Term"

class ValidationError(Exception):
    pass

def validate_student_data(data: dict) -> bool:
    required_fields = ['full_name', 'class', 'parent_name', 'parent_phone']
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValidationError(f"Missing required field: {field}")
    if not Utils.validate_phone(data['parent_phone']):
        raise ValidationError("Invalid phone number format")
    return True

def validate_fee_data(data: dict) -> bool:
    required_fields = ['student_id', 'term', 'academic_year', 'total_amount']
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValidationError(f"Missing required field: {field}")
    try:
        amount = float(data['total_amount'])
        if amount <= 0:
            raise ValidationError("Amount must be positive")
    except ValueError:
        raise ValidationError("Invalid amount format")
    return True