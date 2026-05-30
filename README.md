# ArewaSchool Manager V4
## Advanced School Management System

---

### Project Info
- **Version:** V4.0 — Advanced Business Edition
- **Language:** Python 3.10+
- **GUI:** CustomTkinter
- **Database:** SQLite
- **Packaging:** PyInstaller (.exe)

---

### Project Structure
```
ArewaSchoolManager/
├── main.py              # Entry point
├── launcher.py          # Production launcher
├── build.bat            # One-click EXE builder
├── build.spec           # PyInstaller spec
├── requirements.txt     # Dependencies
│
├── core/
│   ├── __init__.py
│   ├── config.py        # Settings & constants
│   ├── database.py      # DB connection & queries
│   └── utils.py         # Helper functions
│
├── ui/
│   ├── __init__.py
│   ├── splash.py        # Splash screen
│   ├── login.py         # Login window
│   └── dashboard.py     # Main dashboard + RBAC
│
├── modules/
│   ├── __init__.py
│   ├── students.py      # Student CRUD
│   ├── fees.py          # Fees management
│   ├── receipt.py       # Receipt + PDF export
│   ├── staff.py         # Staff CRUD
│   ├── attendance.py    # Attendance tracking
│   ├── results.py       # Results & grades
│   └── reports.py       # Analytics & charts
│
├── assets/              # Icons, images
├── database/            # school.db (auto-created)
└── exports/             # PDF/Excel exports
```

---

### Installation
```bash
# 1. Clone or download project
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

---

### Default Login
| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin123 | Admin |

---

### Role Permissions
| Role    | Modules                                      |
|---------|----------------------------------------------|
| Admin   | All 8 modules                                |
| Teacher | Dashboard, Students, Attendance, Results     |
| Staff   | Dashboard, Fees, Receipts                    |

---

### Build EXE
```bash
# Option 1 — Double-click
build.bat

# Option 2 — Terminal
pip install pyinstaller
pyinstaller build.spec
```
EXE will be at: `dist/ArewaSchoolManager.exe`

---

### Modules
| Module     | Features                                      |
|------------|-----------------------------------------------|
| Students   | Add, Edit, Delete, Search, Auto Reg No        |
| Fees       | Record payments, History, Summary cards       |
| Receipts   | Preview, PDF export, Status badge             |
| Staff      | Add, Edit, Delete, Salary, Department         |
| Attendance | Mark, Toggle, Save, View by date              |
| Results    | Add, Grade auto-calc, Report card             |
| Reports    | Charts, KPIs, Fees/Students/Attendance/Grades |

---

### Requirements
```
customtkinter==5.2.2
pillow==10.3.0
reportlab==4.1.0
openpyxl==3.1.2
matplotlib==3.8.4
tkcalendar==1.6.1
```

---

*© 2024 ArewaSchool Manager — Advanced Business Edition*
