def get_risk_color(risk_level):
    """Get color code for risk level"""
    colors = {
        "Low": "#10B981",      # Green
        "Moderate": "#F59E0B",  # Orange
        "High": "#EF4444"       # Red
    }
    return colors.get(risk_level, "#6B7280")

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."