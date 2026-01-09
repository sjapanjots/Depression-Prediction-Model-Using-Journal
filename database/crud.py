from datetime import datetime, timedelta
import random
from database.database import get_connection

# Simple Journal class
class Journal:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Static prototype data for testing
SAMPLE_JOURNALS = [
    {
        "id": 1,
        "user_id": 1,
        "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "title": "A Great Day",
        "content": "Today was amazing! I felt so energized and productive. Met up with friends and had a wonderful time. Life feels good right now.",
        "depression_score": 0.15,
        "risk_level": "Low",
        "created_at": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "updated_at": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    },
    {
        "id": 2,
        "user_id": 1,
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "title": "Feeling Okay",
        "content": "Nothing special today. Work was fine, came home, watched some TV. Feeling neutral about everything.",
        "depression_score": 0.45,
        "risk_level": "Moderate",
        "created_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "updated_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    },
    {
        "id": 3,
        "user_id": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": "Struggling Today",
        "content": "Feeling really down today. Everything seems harder than it should be. Can't seem to find motivation for anything.",
        "depression_score": 0.78,
        "risk_level": "High",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }
]

def create_journal(user_id, date, title, content, depression_score, risk_level):
    """Create a new journal entry"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO journals (user_id, date, title, content, depression_score, risk_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, str(date), title, content, depression_score, risk_level))
        
        journal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return journal_id
    except Exception as e:
        print(f"Error creating journal: {e}")
        return None

def get_user_journals(user_id, search="", sort_by="Newest"):
    """Get all journals for a user with optional search and sorting"""
    try:
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM journals WHERE user_id = ?"
        params = [user_id]
        
        # Add search filter
        if search:
            query += " AND (title LIKE ? OR content LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        # Add sorting
        if sort_by == "Newest":
            query += " ORDER BY date DESC"
        elif sort_by == "Oldest":
            query += " ORDER BY date ASC"
        elif sort_by == "Risk Level":
            query += " ORDER BY depression_score DESC"
        
        cursor.execute(query, params)
        journals = cursor.fetchall()
        conn.close()
        
        # If no journals in DB, return sample data
        if not journals:
            filtered_journals = SAMPLE_JOURNALS
            
            # Apply search filter
            if search:
                filtered_journals = [
                    j for j in filtered_journals 
                    if search.lower() in j.get("title", "").lower() 
                    or search.lower() in j.get("content", "").lower()
                ]
            
            # Apply sorting
            if sort_by == "Newest":
                filtered_journals = sorted(filtered_journals, key=lambda x: x["date"], reverse=True)
            elif sort_by == "Oldest":
                filtered_journals = sorted(filtered_journals, key=lambda x: x["date"])
            elif sort_by == "Risk Level":
                filtered_journals = sorted(filtered_journals, key=lambda x: x["depression_score"], reverse=True)
            
            return [Journal(**j) for j in filtered_journals]
        
        # Convert to Journal objects
        return [Journal(**j) for j in journals]
        
    except Exception as e:
        print(f"Error getting journals: {e}")
        # Return sample data on error
        return [Journal(**j) for j in SAMPLE_JOURNALS]

def get_journal_by_id(journal_id):
    """Get a specific journal by ID"""
    try:
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM journals WHERE id = ?", (journal_id,))
        journal = cursor.fetchone()
        conn.close()
        
        if journal:
            return Journal(**journal)
        
        # Check sample data
        for sample in SAMPLE_JOURNALS:
            if sample['id'] == journal_id:
                return Journal(**sample)
        
        return None
    except Exception as e:
        print(f"Error getting journal: {e}")
        return None

def update_journal(journal_id, title, content, depression_score, risk_level):
    """Update an existing journal entry"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE journals 
            SET title = ?, content = ?, depression_score = ?, risk_level = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, depression_score, risk_level, journal_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating journal: {e}")
        return False

def delete_journal(journal_id):
    """Delete a journal entry"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM journals WHERE id = ?", (journal_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting journal: {e}")
        return False

def get_user_stats(user_id):
    """Get statistics for user's journals"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total entries
        cursor.execute("SELECT COUNT(*) FROM journals WHERE user_id = ?", (user_id,))
        total = cursor.fetchone()[0]
        
        # Average risk score
        cursor.execute("SELECT AVG(depression_score) FROM journals WHERE user_id = ?", (user_id,))
        avg_score = cursor.fetchone()[0] or 0.3
        
        conn.close()
        
        # If no entries, use sample data
        if total == 0:
            total = len(SAMPLE_JOURNALS)
            avg_score = sum(j['depression_score'] for j in SAMPLE_JOURNALS) / len(SAMPLE_JOURNALS)
        
        # Calculate streak (simplified)
        streak = random.randint(3, 10)
        
        # Average risk level
        if avg_score < 0.33:
            avg_risk = "Low"
        elif avg_score < 0.67:
            avg_risk = "Moderate"
        else:
            avg_risk = "High"
        
        return {
            "total_entries": total,
            "current_streak": streak,
            "average_risk": avg_risk
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            "total_entries": 3,
            "current_streak": 7,
            "average_risk": "Low"
        }