"""
Results/Grades Management Module
ArewaSchool Manager v4
"""

import logging
from core.database import Database
from core.utils import Utils
from core.config import GRADES

logger = logging.getLogger(__name__)

class ResultsManager:
    """Handle student results and grades"""
    
    def __init__(self):
        self.db = Database()
    
    def record_result(self, data):
        """Record student result/score"""
        try:
            score = float(data['score'])
            grade = Utils.calculate_grade(score)
            
            self.db.execute('''
                INSERT INTO results (
                    student_id, subject, score, grade,
                    term, academic_year, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['student_id'], data['subject'], score,
                grade, data.get('term'), data.get('academic_year'),
                data.get('recorded_by')
            ))
            
            logger.info(f"Result recorded for student {data['student_id']}: {data['subject']} = {grade}")
            return {"success": True, "grade": grade}
        except ValueError:
            return {"success": False, "error": "Invalid score format"}
        except Exception as e:
            logger.error(f"Error recording result: {e}")
            return {"success": False, "error": str(e)}
    
    def get_results(self, student_id, term=None, academic_year=None):
        """Get student results"""
        try:
            if term and academic_year:
                results = self.db.fetch_all(
                    "SELECT * FROM results WHERE student_id = ? AND term = ? AND academic_year = ?",
                    (student_id, term, academic_year)
                )
            else:
                results = self.db.fetch_all(
                    "SELECT * FROM results WHERE student_id = ? ORDER BY academic_year DESC, term DESC",
                    (student_id,)
                )
            
            return {"success": True, "data": results}
        except Exception as e:
            logger.error(f"Error fetching results: {e}")
            return {"success": False, "error": str(e)}
    
    def get_report_card(self, student_id, term, academic_year):
        """Generate report card data"""
        try:
            results = self.db.fetch_all(
                "SELECT * FROM results WHERE student_id = ? AND term = ? AND academic_year = ?",
                (student_id, term, academic_year)
            )
            
            total_score = sum(float(r['score']) for r in results) if results else 0
            average = total_score / len(results) if results else 0
            overall_grade = Utils.calculate_grade(average)
            
            return {
                "success": True,
                "results": results,
                "average": average,
                "overall_grade": overall_grade,
                "total_subjects": len(results)
            }
        except Exception as e:
            logger.error(f"Error generating report card: {e}")
            return {"success": False, "error": str(e)}
    
    def update_result(self, result_id, score):
        """Update a result/score"""
        try:
            grade = Utils.calculate_grade(float(score))
            
            self.db.execute(
                "UPDATE results SET score = ?, grade = ? WHERE id = ?",
                (score, grade, result_id)
            )
            
            logger.info(f"Result {result_id} updated")
            return {"success": True, "grade": grade}
        except Exception as e:
            logger.error(f"Error updating result: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    manager = ResultsManager()
    print("ResultsManager initialized")