"""
Configuration for ArewaSchool Manager
2026 Modern Design
"""
import os
from pathlib import Path

APP_NAME = "ArewaSchool Manager"
APP_VERSION = "4.0"
APP_AUTHOR = "Umar Musa Isah"
APP_YEAR = "2026"

DB_PATH = Path("database/school.db")
DB_PATH.parent.mkdir(exist_ok=True)

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

for directory in [ASSETS_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

SIDEBAR_WIDTH = 220
TOPBAR_HEIGHT = 60

COLORS = {
    "primary_blue": "#1a73e8",
    "success_green": "#34a853",
    "alert_red": "#ea4335",
    "warning_yellow": "#fbbc04",
    "dark_bg": "#1e1e2e",
    "light_bg": "#f8f9fa",
    "card_bg": "#ffffff",
    "text_dark": "#2d3748",
    "text_light": "#718096",
    "border_gray": "#e2e8f0",
    "hover_light": "#f7fafc",
}

FONTS = {
    "header_bold": ("Segoe UI", 18, "bold"),
    "header_large": ("Segoe UI", 24, "bold"),
    "body_regular": ("Segoe UI", 13),
    "body_small": ("Segoe UI", 12),
    "label_medium": ("Segoe UI", 12, "bold"),
}

ROLES = {
    "admin": "Administrator",
    "teacher": "Teacher",
    "staff": "Staff",
}

DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123",
    "full_name": "System Administrator",
    "role": "admin",
}

ACADEMIC_YEARS = ["2025/2026", "2026/2027", "2027/2028"]
TERMS = ["First Term", "Second Term", "Third Term"]
CLASSES = ["JSS 1", "JSS 2", "JSS 3", "SS 1", "SS 2", "SS 3"]

GENDERS = ["Male", "Female", "Other"]

ATTENDANCE_STATUS = ["Present", "Absent", "Late", "Excused"]

GRADES = {
    "A": (90, 100),
    "B": (80, 89),
    "C": (70, 79),
    "D": (60, 69),
    "E": (50, 59),
    "F": (0, 49),
}

PAYMENT_METHODS = ["Cash", "Bank Transfer", "Cheque", "Mobile Money"]

EXPORT_FORMATS = ["PDF", "Excel"]

ITEMS_PER_PAGE = 20

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

THEME = "dark"
LANGUAGE = "en"
AUTO_BACKUP = True
BACKUP_INTERVAL = 3600

DEBUG_MODE = True

print(f"[CONFIG] {APP_NAME} v{APP_VERSION} - Configuration Loaded")