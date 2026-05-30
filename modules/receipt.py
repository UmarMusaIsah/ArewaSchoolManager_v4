"""
Receipt Generation Module
ArewaSchool Manager v4
"""

import logging
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from core.database import Database
from core.config import EXPORTS_DIR, APP_NAME

logger = logging.getLogger(__name__)

class ReceiptGenerator:
    """Generate professional receipts"""
    
    def __init__(self):
        self.db = Database()
        self.exports_dir = EXPORTS_DIR / "receipts"
        self.exports_dir.mkdir(exist_ok=True)
    
    def generate_pdf_receipt(self, receipt_number, student_id, amount, payment_method):
        """Generate PDF receipt"""
        try:
            student = self.db.fetch_one(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )
            
            if not student:
                return {"success": False, "error": "Student not found"}
            
            filename = f"{receipt_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
            filepath = self.exports_dir / filename
            
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            elements = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'Custom',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a73e8'),
                alignment=1,
                spaceAfter=6
            )
            
            elements.append(Paragraph(APP_NAME, title_style))
            elements.append(Spacer(1, 12))
            
            header_data = [
                ["PAYMENT RECEIPT", ""],
                ["Receipt Number:", receipt_number],
                ["Date:", datetime.now().strftime("%d-%m-%Y")],
                ["Payment Method:", payment_method],
            ]
            
            header_table = Table(header_data, colWidths=[200, 200])
            header_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 12))
            
            student_data = [
                ["Student Details", ""],
                ["Registration No:", student['reg_number']],
                ["Full Name:", student['full_name']],
                ["Class:", student['class']],
                ["Parent Name:", student['parent_name']],
            ]
            
            student_table = Table(student_data, colWidths=[150, 250])
            student_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(student_table)
            elements.append(Spacer(1, 12))
            
            payment_data = [
                ["Description", "Amount"],
                ["Amount Paid", f"₦{amount:,.2f}"],
            ]
            
            payment_table = Table(payment_data, colWidths=[200, 200])
            payment_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34a853')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(payment_table)
            elements.append(Spacer(1, 24))
            
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=1
            )
            elements.append(Paragraph(
                "Thank you for your payment. Please keep this receipt for your records.",
                footer_style
            ))
            
            doc.build(elements)
            
            logger.info(f"Receipt generated: {filename}")
            return {"success": True, "filepath": str(filepath), "filename": filename}
        
        except Exception as e:
            logger.error(f"Error generating receipt: {e}")
            return {"success": False, "error": str(e)}
    
    def get_receipt_history(self, student_id):
        """Get receipt history for student"""
        try:
            receipts = self.db.fetch_all(
                "SELECT * FROM receipts WHERE student_id = ? ORDER BY receipt_date DESC",
                (student_id,)
            )
            return {"success": True, "data": receipts}
        except Exception as e:
            logger.error(f"Error fetching receipt history: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    generator = ReceiptGenerator()
    print("ReceiptGenerator initialized")