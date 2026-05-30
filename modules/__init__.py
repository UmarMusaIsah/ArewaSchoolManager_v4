"""
Modules Package
"""
from .students import StudentManager
from .fees import FeesManager
from .receipt import ReceiptGenerator
from .staff import StaffManager
from .attendance import AttendanceManager
from .results import ResultsManager
from .reports import ReportsGenerator

__all__ = [
    'StudentManager', 'FeesManager', 'ReceiptGenerator',
    'StaffManager', 'AttendanceManager', 'ResultsManager', 'ReportsGenerator'
]