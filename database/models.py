# Simple data class for Journal entries

class Journal:
    def __init__(self, id, user_id, date, title, content, depression_score, risk_level, created_at, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.title = title
        self.content = content
        self.depression_score = depression_score
        self.risk_level = risk_level
        self.created_at = created_at
        self.updated_at = updated_at or created_at

class User:
    def __init__(self, id, username, email, password_hash, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at