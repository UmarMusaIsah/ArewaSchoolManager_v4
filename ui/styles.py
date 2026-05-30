"""
UI Styling - 2026 Modern Design
"""
from core.config import COLORS, FONTS

class Styles:
    PRIMARY_BLUE = COLORS["primary_blue"]
    SUCCESS_GREEN = COLORS["success_green"]
    ALERT_RED = COLORS["alert_red"]
    WARNING_YELLOW = COLORS["warning_yellow"]
    DARK_BG = COLORS["dark_bg"]
    LIGHT_BG = COLORS["light_bg"]
    CARD_BG = COLORS["card_bg"]
    TEXT_DARK = COLORS["text_dark"]
    TEXT_LIGHT = COLORS["text_light"]
    BORDER_GRAY = COLORS["border_gray"]
    HOVER_LIGHT = COLORS["hover_light"]
    
    HEADER_BOLD = FONTS["header_bold"]
    HEADER_LARGE = FONTS["header_large"]
    BODY_REGULAR = FONTS["body_regular"]
    BODY_SMALL = FONTS["body_small"]
    LABEL_MEDIUM = FONTS["label_medium"]
    
    @staticmethod
    def get_button_style(button_type="primary"):
        styles = {
            "primary": {
                "fg_color": Styles.PRIMARY_BLUE,
                "text_color": "white",
                "hover_color": "#1557b0",
            },
            "success": {
                "fg_color": Styles.SUCCESS_GREEN,
                "text_color": "white",
                "hover_color": "#2d8c42",
            },
            "danger": {
                "fg_color": Styles.ALERT_RED,
                "text_color": "white",
                "hover_color": "#c5332b",
            },
        }
        return styles.get(button_type, styles["primary"])

class Animations:
    TRANSITION_FAST = 100
    TRANSITION_NORMAL = 300
    TRANSITION_SLOW = 500

class Spacing:
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32