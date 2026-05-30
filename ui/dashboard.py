"""
Main Dashboard UI
ArewaSchool Manager v4
"""

import customtkinter as ctk
from core.config import APP_NAME, SIDEBAR_WIDTH, TOPBAR_HEIGHT, COLORS
from ui.styles import Styles
from core.database import Database
import logging

logger = logging.getLogger(__name__)

class DashboardUI(ctk.CTk):
    """Professional dashboard with sidebar and content area"""
    
    def __init__(self, user=None):
        super().__init__()
        
        self.user = user
        self.db = Database()
        self.current_module = None
        
        self.title(f"{APP_NAME} - Dashboard")
        self.geometry("1200x800")
        self.configure(fg_color=Styles.LIGHT_BG)
        
        self.create_layout()
        
        logger.info(f"Dashboard loaded for user: {user['full_name'] if user else 'Unknown'}")
    
    def create_layout(self):
        """Create main dashboard layout"""
        
        self.main_container = ctk.CTkFrame(self, fg_color=Styles.LIGHT_BG)
        self.main_container.pack(fill="both", expand=True)
        
        self.create_topbar()
        
        self.content_container = ctk.CTkFrame(self.main_container, fg_color=Styles.LIGHT_BG)
        self.content_container.pack(fill="both", expand=True)
        
        self.create_sidebar()
        self.create_content_area()
    
    def create_topbar(self):
        """Create top navigation bar"""
        self.topbar = ctk.CTkFrame(
            self.main_container,
            fg_color=Styles.PRIMARY_BLUE,
            height=TOPBAR_HEIGHT
        )
        self.topbar.pack(fill="x", side="top")
        self.topbar.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.topbar,
            text=f"{APP_NAME}",
            font=Styles.HEADER_BOLD,
            text_color="white"
        )
        self.title_label.pack(side="left", padx=20, pady=10)
        
        if self.user:
            user_info = f"Welcome, {self.user['full_name']} ({self.user['role'].title()})"
            self.user_label = ctk.CTkLabel(
                self.topbar,
                text=user_info,
                font=Styles.BODY_SMALL,
                text_color="white"
            )
            self.user_label.pack(side="right", padx=20, pady=10)
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        self.sidebar = ctk.CTkFrame(
            self.content_container,
            fg_color=Styles.DARK_BG,
            width=SIDEBAR_WIDTH
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            font=Styles.LABEL_MEDIUM,
            text_color="white"
        )
        self.sidebar_title.pack(pady=20, padx=15)
        
        menu_items = [
            ("🏠 Dashboard", "dashboard"),
            ("👨‍🎓 Students", "students"),
            ("💰 Fees", "fees"),
            ("🧾 Receipts", "receipts"),
            ("👩‍🏫 Staff", "staff"),
            ("📅 Attendance", "attendance"),
            ("📝 Results", "results"),
            ("📊 Reports", "reports"),
            ("⚙️ Settings", "settings"),
            ("🚪 Logout", "logout"),
        ]
        
        for item_name, item_key in menu_items:
            self.create_menu_button(item_name, item_key)
    
    def create_menu_button(self, text, key):
        """Create menu button"""
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            fg_color="transparent",
            text_color="white",
            hover_color=Styles.PRIMARY_BLUE,
            font=Styles.BODY_REGULAR,
            command=lambda: self.load_module(key)
        )
        button.pack(fill="x", padx=10, pady=5)
    
    def create_content_area(self):
        """Create main content area"""
        self.content_area = ctk.CTkFrame(
            self.content_container,
            fg_color=Styles.LIGHT_BG
        )
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.load_dashboard()
    
    def load_dashboard(self):
        """Load default dashboard"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        welcome_card = ctk.CTkFrame(
            self.content_area,
            fg_color=Styles.CARD_BG,
            corner_radius=10
        )
        welcome_card.pack(fill="x", pady=(0, 20))
        
        welcome_text = ctk.CTkLabel(
            welcome_card,
            text=f"Welcome to {APP_NAME}",
            font=Styles.HEADER_BOLD,
            text_color=Styles.TEXT_DARK
        )
        welcome_text.pack(pady=20, padx=20)
        
        stats_frame = ctk.CTkFrame(self.content_area, fg_color=Styles.LIGHT_BG)
        stats_frame.pack(fill="x", pady=10)
        
        stats = [
            ("Total Students", "150", Styles.PRIMARY_BLUE),
            ("Total Staff", "25", Styles.SUCCESS_GREEN),
            ("Fees Collected", "₦500,000", Styles.ALERT_RED),
            ("Outstanding", "₦120,000", Styles.WARNING_YELLOW),
        ]
        
        for stat_name, stat_value, color in stats:
            self.create_stat_card(stats_frame, stat_name, stat_value, color)
    
    def create_stat_card(self, parent, title, value, color):
        """Create statistic card"""
        card = ctk.CTkFrame(parent, fg_color=Styles.CARD_BG, corner_radius=10)
        card.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=Styles.BODY_SMALL,
            text_color=Styles.TEXT_LIGHT
        )
        title_label.pack(pady=(10, 5), padx=10)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=Styles.HEADER_BOLD,
            text_color=color
        )
        value_label.pack(pady=(5, 10), padx=10)
    
    def load_module(self, module_name):
        """Load a module"""
        logger.info(f"Loading module: {module_name}")
        
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if module_name == "dashboard":
            self.load_dashboard()
        elif module_name == "logout":
            self.logout()
        else:
            title = ctk.CTkLabel(
                self.content_area,
                text=f"{module_name.title()} Module",
                font=Styles.HEADER_LARGE,
                text_color=Styles.TEXT_DARK
            )
            title.pack(pady=20)
            
            info = ctk.CTkLabel(
                self.content_area,
                text=f"Coming Soon: {module_name.title()} functionality",
                font=Styles.BODY_REGULAR,
                text_color=Styles.TEXT_LIGHT
            )
            info.pack(pady=10)
    
    def logout(self):
        """Logout user"""
        logger.info("User logged out")
        self.destroy()

if __name__ == "__main__":
    dashboard = DashboardUI(user={"full_name": "Admin", "role": "admin"})
    dashboard.mainloop()