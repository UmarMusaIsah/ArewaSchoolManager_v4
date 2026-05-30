"""
Login Screen UI
ArewaSchool Manager v4
"""

import customtkinter as ctk
from core.config import APP_NAME, COLORS
from ui.styles import Styles
from core.database import Database
from core.utils import Utils
import logging

logger = logging.getLogger(__name__)

class LoginUI(ctk.CTk):
    """Professional login interface"""
    
    def __init__(self, on_login_success=None):
        super().__init__()
        
        self.on_login_success = on_login_success
        self.db = Database()
        
        self.title(f"{APP_NAME} - Login")
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(fg_color=Styles.LIGHT_BG)
        
        self.center_window()
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Styles.LIGHT_BG)
        self.main_frame.pack(fill="both", expand=True)
        
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=Styles.PRIMARY_BLUE, height=100)
        self.header_frame.pack(fill="x")
        
        self.app_name = ctk.CTkLabel(
            self.header_frame,
            text=APP_NAME,
            font=Styles.HEADER_LARGE,
            text_color="white"
        )
        self.app_name.pack(pady=20)
        
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color=Styles.CARD_BG, corner_radius=10)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Login to Your Account",
            font=Styles.HEADER_BOLD,
            text_color=Styles.TEXT_DARK
        )
        self.form_title.pack(pady=(20, 30))
        
        self.username_label = ctk.CTkLabel(
            self.form_frame,
            text="Username",
            font=Styles.LABEL_MEDIUM,
            text_color=Styles.TEXT_DARK
        )
        self.username_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.username_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter your username",
            width=350,
            height=40,
            font=Styles.BODY_REGULAR,
            fg_color=Styles.CARD_BG,
            text_color=Styles.TEXT_DARK,
            border_color=Styles.BORDER_GRAY,
            border_width=1,
            corner_radius=6,
        )
        self.username_entry.pack(padx=20, pady=(5, 15))
        
        self.password_label = ctk.CTkLabel(
            self.form_frame,
            text="Password",
            font=Styles.LABEL_MEDIUM,
            text_color=Styles.TEXT_DARK
        )
        self.password_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.password_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter your password",
            show="●",
            width=350,
            height=40,
            font=Styles.BODY_REGULAR,
            fg_color=Styles.CARD_BG,
            text_color=Styles.TEXT_DARK,
            border_color=Styles.BORDER_GRAY,
            border_width=1,
            corner_radius=6,
        )
        self.password_entry.pack(padx=20, pady=(5, 20))
        
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_check = ctk.CTkCheckBox(
            self.form_frame,
            text="Remember me",
            variable=self.remember_var,
            font=Styles.BODY_SMALL,
            text_color=Styles.TEXT_DARK,
            fg_color=Styles.PRIMARY_BLUE
        )
        self.remember_check.pack(anchor="w", padx=20, pady=5)
        
        self.login_button = ctk.CTkButton(
            self.form_frame,
            text="Login",
            command=self.on_login_click,
            width=350,
            height=45,
            font=Styles.LABEL_MEDIUM,
            text_color="white",
            fg_color=Styles.PRIMARY_BLUE,
            hover_color="#1557b0",
        )
        self.login_button.pack(pady=20)
        
        self.error_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=Styles.BODY_SMALL,
            text_color=Styles.ALERT_RED
        )
        self.error_label.pack(pady=10)
        
        self.password_entry.bind("<Return>", lambda e: self.on_login_click())
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def on_login_click(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        try:
            user = self.db.fetch_one(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            
            if not user:
                self.show_error("Invalid username or password")
                logger.warning(f"Login attempt failed: User {username} not found")
                return
            
            if user['password'] != password:
                self.show_error("Invalid username or password")
                logger.warning(f"Login attempt failed: Wrong password for {username}")
                return
            
            if not user['is_active']:
                self.show_error("Your account is inactive")
                logger.warning(f"Login attempt failed: Account {username} is inactive")
                return
            
            logger.info(f"User {username} logged in successfully")
            
            if self.on_login_success:
                self.on_login_success(user)
            
            self.destroy()
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            self.show_error("An error occurred during login")
    
    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
        self.error_label.pack(pady=10)

if __name__ == "__main__":
    login = LoginUI()
    login.mainloop()