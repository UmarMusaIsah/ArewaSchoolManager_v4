"""
Main Application Entry Point
ArewaSchool Manager v4
"""
import sys
import logging
import customtkinter as ctk

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from core.config import APP_NAME, APP_VERSION
from core.database import Database

class ArewaSchoolManager:
    def __init__(self):
        self.app = None
        self.db = None
        self.current_user = None
        logger.info(f"Initializing {APP_NAME} v{APP_VERSION}")
    
    def initialize_database(self):
        try:
            self.db = Database()
            logger.info("Database initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    def run(self):
        try:
            if not self.initialize_database():
                logger.error("Failed to initialize database")
                sys.exit(1)
            
            print(f"✅ {APP_NAME} v{APP_VERSION} initialized successfully!")
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            sys.exit(1)
        finally:
            if self.db:
                self.db.close()

def main():
    app = ArewaSchoolManager()
    app.run()

if __name__ == "__main__":
    main()