"""
Splash Screen UI - Loading/Welcome Screen
ArewaSchool Manager v4
2026 Modern Design
"""

import customtkinter as ctk
from core.config import APP_NAME, APP_VERSION, COLORS
from ui.styles import Styles
import threading
import time

class SplashScreen(ctk.CTk):
    """Professional splash screen with loading animation"""
    
    def __init__(self, duration=3):
        super().__init__()
        
        self.duration = duration
        self.progress = 0
        
        self.title(f"{APP_NAME} - Loading")
        self.geometry("600x400")
        self.resizable(False, False)
        self.configure(fg_color=Styles.DARK_BG)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        self.container = ctk.CTkFrame(self, fg_color=Styles.DARK_BG)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.title_label = ctk.CTkLabel(
            self.container,
            text=APP_NAME,
            font=Styles.HEADER_LARGE,
            text_color=Styles.PRIMARY_BLUE
        )
        self.title_label.pack(pady=(40, 10))
        
        self.version_label = ctk.CTkLabel(
            self.container,
            text=f"v{APP_VERSION} - 2026 Edition",
            font=Styles.BODY_SMALL,
            text_color=Styles.TEXT_LIGHT
        )
        self.version_label.pack(pady=(0, 40))
        
        self.loading_label = ctk.CTkLabel(
            self.container,
            text="Initializing System...",
            font=Styles.BODY_REGULAR,
            text_color=Styles.TEXT_DARK
        )
        self.loading_label.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.container,
            fg_color=Styles.BORDER_GRAY,
            progress_color=Styles.PRIMARY_BLUE,
            height=6,
            corner_radius=3
        )
        self.progress_bar.pack(fill="x", pady=10)
        self.progress_bar.set(0)
        
        self.progress_text = ctk.CTkLabel(
            self.container,
            text="0%",
            font=Styles.BODY_SMALL,
            text_color=Styles.TEXT_LIGHT
        )
        self.progress_text.pack(pady=(10, 0))
        
        self.footer_label = ctk.CTkLabel(
            self.container,
            text="Powered by Professional Development Team",
            font=Styles.BODY_SMALL,
            text_color=Styles.TEXT_LIGHT
        )
        self.footer_label.pack(side="bottom", pady=10)
        
        self.loading_thread = threading.Thread(target=self.animate_loading, daemon=True)
        self.loading_thread.start()
    
    def animate_loading(self):
        """Animate the loading progress"""
        start_time = time.time()
        
        messages = [
            "Initializing System...",
            "Loading Database...",
            "Configuring UI...",
            "Preparing Modules...",
            "Almost Ready...",
        ]
        
        while self.progress < 100:
            elapsed = time.time() - start_time
            self.progress = min(int((elapsed / self.duration) * 100), 100)
            
            message_index = min(int((self.progress / 100) * len(messages)), len(messages) - 1)
            
            self.progress_bar.set(self.progress / 100)
            self.progress_text.configure(text=f"{self.progress}%")
            self.loading_label.configure(text=messages[message_index])
            
            self.update()
            time.sleep(0.05)
        
        self.after(500, self.destroy)

def show_splash():
    """Show splash screen"""
    splash = SplashScreen(duration=3)
    splash.mainloop()

if __name__ == "__main__":
    show_splash()