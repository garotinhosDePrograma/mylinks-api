import re

def is_valid_username(username):
    if not username or not isinstance(username, str):
        return False
    
    if len(username) < 3 or len(username) > 20:
        return False
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$'
    
    if not re.match(pattern, username):
        return False
    
    reserved = [
        'admin', 'root', 'system', 'api', 'www', 'ftp', 'mail',
        'support', 'help', 'info', 'contact', 'about', 'terms',
        'privacy', 'login', 'register', 'signup', 'signin',
        'logout', 'profile', 'settings', 'dashboard', 'user'
    ]
    
    if username.lower() in reserved:
        return False
    
    return True

def get_username_error(username):
    if not username:
        return "Username é obrigatório"
    if len(username) < 3:
        return "Username deve ter no minimo 4 caracteres"
    if len(username) > 20:
        return "Username deve ter no máximo 20 caracteres"
    if not re.match(r'^[a-zA-z0-9_-]+$', username):
        return "Username pode conter apenas Letras, Números, _ e -"
    
    reserved = [
        'admin', 'root', 'system', 'api', 'www', 'ftp', 'mail',
        'support', 'help', 'info', 'contact', 'about', 'terms',
        'privacy', 'login', 'register', 'signup', 'signin',
        'logout', 'profile', 'settings', 'dashboard', 'user'
    ]

    if username.lower() in reserved:
        return "Este username está reservado"
    
    return "Username inválido"
