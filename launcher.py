"""
Application Launcher
Handles initialization
"""

import sys
from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def launch_application():
    """Launch the application"""
    try:
        from main import main
        main()
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logger.info("Launching ArewaSchool Manager...")
    launch_application()