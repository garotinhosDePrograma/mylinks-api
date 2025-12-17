import re

def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-z0-9._%+-]+@[a-zA-z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if len(email) > 254:
        return False
    
    if '..' in email:
        return False
    
    return bool(re.match(pattern, email))